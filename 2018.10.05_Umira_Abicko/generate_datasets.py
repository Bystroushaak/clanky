#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import sys
import os.path
import shutil
import argparse
import datetime
from collections import defaultdict

import matplotlib.pyplot as plt

from tqdm import tqdm
from sqlitedict import SqliteDict


class BlogAnalyzer(object):
    def __init__(self):
        self.length_of_blogs_in_years = defaultdict(int)
        self.length_of_blogs_in_months = defaultdict(int)

        self.number_of_blogs_in_years = defaultdict(int)
        self.number_of_blogs_in_months = defaultdict(int)

        self.number_of_comments_in_years = defaultdict(int)
        self.number_of_comments_in_months = defaultdict(int)

        self.active_registered_people_in_years = defaultdict(set)
        self.active_registered_people_in_months = defaultdict(set)

        self.active_unregistered_people_in_years = defaultdict(set)
        self.active_unregistered_people_in_months = defaultdict(set)

        self.number_of_registered_people_in_years = defaultdict(int)
        self.number_of_registered_people_in_months = defaultdict(int)

        self.number_of_unregistered_people_in_years = defaultdict(int)
        self.number_of_unregistered_people_in_months = defaultdict(int)

        self.read_counter_in_years = defaultdict(int)
        self.read_counter_in_months = defaultdict(int)

    def timestamp_to_yyyy(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y')

    def timestamp_to_yyyy_mm(self, timestamp):
        return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m')

    def analyze(self, blog):
        blog_yyyy = self.timestamp_to_yyyy(blog.created_ts)
        blog_yyyy_mm = self.timestamp_to_yyyy_mm(blog.created_ts)

        self.length_of_blogs_in_years[blog_yyyy] += len(blog.text)
        self.length_of_blogs_in_months[blog_yyyy_mm] += len(blog.text)

        self.number_of_blogs_in_years[blog_yyyy] += 1
        self.number_of_blogs_in_months[blog_yyyy_mm] += 1

        self.number_of_comments_in_years[blog_yyyy] += len(blog.comments)
        self.number_of_comments_in_months[blog_yyyy_mm] += len(blog.comments)

        self.read_counter_in_years[blog_yyyy] += blog.readed or 0
        self.read_counter_in_months[blog_yyyy_mm] += blog.readed or 0

        for comment in blog.comments:
            comment_yyyy = self.timestamp_to_yyyy(blog.created_ts)
            comment_yyyy_mm = self.timestamp_to_yyyy_mm(blog.created_ts)
            username = comment.username

            if comment.registered:
                self.active_registered_people_in_years[comment_yyyy].add(username)
                self.active_registered_people_in_months[comment_yyyy_mm].add(username)
            else:
                self.active_unregistered_people_in_years[comment_yyyy].add(username)
                self.active_unregistered_people_in_months[comment_yyyy_mm].add(username)

    def dump_counter_into_csv(self, counter, csv_name):
        with open(csv_name, 'wb') as csvfile:
            writer = csv.writer(
                csvfile,
                delimiter=';',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )
            for year, count in sorted(counter.items()):
                writer.writerow([year, count])

    def counter_into_png(self, dataset_name, counter, axis, png_name):
        x_points = []
        y_points = []
        for x, y in sorted(counter.items()):
            x_points.append(x)
            y_points.append(y)

        fig, ax = plt.subplots(1, 1)
        plt.title(axis["description"].decode("utf-8"))
        plt.xlabel(axis["x"].decode("utf-8"))
        plt.ylabel(axis["y"].decode("utf-8"))
        plt.xticks(rotation=60)
        plt.plot(x_points, y_points)
        fig.tight_layout()

        if "months" in dataset_name:
            for cnt, label in enumerate(ax.get_xticklabels()):
                if cnt % 6 != 0:
                    label.set_visible(False)

        plt.savefig(png_name)
        plt.clf()

    def generate_report(self, out_dir):
        self.number_of_registered_people_in_years = {
            key: len(people)
            for key, people in self.active_registered_people_in_years.iteritems()
        }
        self.number_of_registered_people_in_months = {
            key: len(people)
            for key, people in self.active_registered_people_in_months.iteritems()
        }
        self.number_of_unregistered_people_in_years = {
            key: len(people)
            for key, people in self.active_unregistered_people_in_years.iteritems()
        }
        self.number_of_unregistered_people_in_months = {
            key: len(people)
            for key, people in self.active_unregistered_people_in_months.iteritems()
        }

        datasets = {
            "length_of_blogs_in_years": {
                "dataset": self.length_of_blogs_in_years,
                "description": "Délka blogů v průběhu let (po letech)",
                "x": "Roky",
                "y": "Délka blogů"
            },
            "length_of_blogs_in_months": {
                "dataset": self.length_of_blogs_in_months,
                "description": "Délka blogů v průběhu let (po měsících)",
                "x": "Měsíce",
                "y": "Délka blogů"
            },
            "number_of_blogs_in_years": {
                "dataset": self.number_of_blogs_in_years,
                "description": "Počty blogů (po letech)",
                "x": "Roky",
                "y": "Počet blogů"
            },
            "number_of_blogs_in_months": {
                "dataset": self.number_of_blogs_in_months,
                "description": "Počty blogů (po měsících)",
                "x": "Měsíce",
                "y": "Počet blogů"
            },
            "number_of_comments_in_years": {
                "dataset": self.number_of_comments_in_years,
                "description": "Počty komentářů (po letech)",
                "x": "Roky",
                "y": "Počet komentářů"
            },
            "number_of_comments_in_months": {
                "dataset": self.number_of_comments_in_months,
                "description": "Počty komentářů (po měsících)",
                "x": "Měsíce",
                "y": "Počet komentářů"
            },
            "number_of_registered_people_in_years": {
                "dataset": self.number_of_registered_people_in_years,
                "description": "Aktivní registrovaní komentátoři (po letech)",
                "x": "Roky",
                "y": "Počet komentátorů"
            },
            "number_of_registered_people_in_months": {
                "dataset": self.number_of_registered_people_in_months,
                "description": "Aktivní registrovaní komentátoři (po měsících)",
                "x": "Měsíce",
                "y": "Počet komentátorů"
            },
            "number_of_unregistered_people_in_years": {
                "dataset": self.number_of_unregistered_people_in_years,
                "description": "Aktivní NEregistrovaní komentátoři (po letech)",
                "x": "Roky",
                "y": "Počet komentátorů"
            },
            "number_of_unregistered_people_in_months": {
                "dataset": self.number_of_unregistered_people_in_months,
                "description": "Aktivní NEregistrovaní komentátoři (po měsících)",
                "x": "Měsíce",
                "y": "Počet komentátorů"
            },
            "read_counter_in_years": {
                "dataset": self.read_counter_in_years,
                "description": "Celkové počty přečtení (po rocích)",
                "x": "Roky",
                "y": "Počty přečtení blogů"
            },
            "read_counter_in_months": {
                "dataset": self.read_counter_in_months,
                "description": "Celkové počty přečtení (po měsících)",
                "x": "Měsíce",
                "y": "Počty přečtení blogů"
            }
        }

        for dataset_name, data in datasets.iteritems():
            self.dump_counter_into_csv(
                data["dataset"],
                os.path.join(out_dir, dataset_name + ".csv")
            )
            self.counter_into_png(
                dataset_name,
                data["dataset"],
                data,
                os.path.join(out_dir, dataset_name + ".png")
            )


def generate_report(blogtree_path, out_dir):
    analyzer = BlogAnalyzer()

    with SqliteDict(blogtree_path) as serialized:
        for blog in tqdm(serialized.itervalues(), total=len(serialized)):
            analyzer.analyze(blog)

    analyzer.generate_report(out_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "blogtree",
        metavar="BLOGTREE.sqlite",
        help="Path to the blogtree .sqlite file."
    )
    parser.add_argument(
        "-o",
        "--output",
        default="datasets",
        help="Name of the output directory. Default `%(default)s.`",
    )

    args = parser.parse_args()

    if not os.path.exists(args.blogtree):
        sys.stderr.write("`%s` not found.\n" % args.blogtree)
        sys.exit(1)

    if os.path.exists(args.output):
        shutil.rmtree(args.output)

    os.mkdir(args.output)

    generate_report(args.blogtree, args.output)
