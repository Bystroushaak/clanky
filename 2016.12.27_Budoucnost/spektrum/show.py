#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Copyright (c) 07.02.2016 Bystroushaak
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# Imports =====================================================================
import csv
import math
import textwrap
from string import Template
from collections import namedtuple
from collections import defaultdict


# Functions & classes =========================================================
def csv_to_namedtuples(csvfile, name):
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    nt = None
    for cnt, row in enumerate(spamreader):
        if cnt == 0:
            nt = namedtuple(name, row)
            continue

        yield nt(*row)


def freq_iterator(freq, plans):
    freq_id_map = {f.id: f for f in freq}
    plan_id_map = defaultdict(set)
    for plan in plans:
        keywords = plan.keywords if plan.keywords else ""
        keywords = set(keywords.split(";"))
        plan_id_map[plan.frequency_id].update(keywords)

    for f in freq:
        keywords = plan_id_map.get(f.id, set())

        if int(f.start) < 8000000000:
            yield int(f.start), int(f.end), keywords


def one_meg_iterator(freq_iter):
    ONE_MEG = 1000000

    def freq_to_meg(freq):
        return int(math.floor(freq / ONE_MEG))

    for start, end, kwds in freq_iter:
        cnt = start
        while cnt < end:
            yield freq_to_meg(cnt), kwds
            cnt += ONE_MEG


def remove_dupes(one_meg_iter):
    """
    One meg iterator may contain multiple keywordsets for one frequency. IE:

    (1, set(['', 'L\xc3\xa9ka\xc5\x99sk\xc3\xa9 implant\xc3\xa1ty', 'SRD',
    'RFID', 'Tagy', 'R\xc3\xa1diov\xc3\xa9 etikety']))
    (1, set(['SRD', 'RTTT', 'TTT', 'Telematika', 'SRD pro telematiku',
    'EUROBALISE']))

    Thats because lower frequency spectrum is divided into sub-megahertz scale.

    This function smoothes the duplicite data into unique dictionary mapping
    the {mhz_freq: keywords}.
    """
    keyword_table = defaultdict(set)

    for freq, keywords in one_meg_iter:
        keyword_table[freq].update(keywords)

    return keyword_table


def render_sng(pix_map, line_height, lines=8, spacer=10):
    out = """#SNG

IHDR: {
  width: $width;
  height: $height;
  bitdepth: 8;
  using color: palette;
  with interlace;
}
sBIT: {red: 8; green: 8; blue: 8;}
PLTE: {"blue", "red", "light slate blue", "black"}

IMAGE: {
  pixels base64
$picture
}
"""
    width = (len(pix_map) / lines) + 1
    picture = ""
    for line in textwrap.fill(pix_map, width).splitlines():
        if len(line) < width:
            line += (width - len(line)) * "3"
        picture += "\n".join(line_height * [line]) + "\n"

        for i in range(spacer):
            picture += (width * "3") + "\n"

    return Template(out).substitute(
        width=width,
        height=picture.count("\n"),
        picture=picture,
    )


# Main program ================================================================
if __name__ == '__main__':
    with open('frequency.csv', 'rb') as csvfile:
        freq = list(csv_to_namedtuples(csvfile, "Frequency"))

    with open('plan.csv', 'rb') as csvfile:
        plan = list(csv_to_namedtuples(csvfile, "Plan"))

    one_meg_iter = one_meg_iterator(freq_iterator(freq, plan))

    freq_map = remove_dupes(one_meg_iter)
    freq_key_list = sorted(freq_map.items(), key=lambda x: x[0])

    data_keywords = {
        "2G",
        "3G",
        "4G",
        "700 MHz",
        "800 MHz",
        "900 MHz",
        "Bluetooth",
        "bod-bod",
        "bod-více bodů",
        "CDMA",
        "Datové spoje",
        "E-GSM",
        "FWA",
        "Galileo",
        "GLONASS",
        "GPS",
        "GSM",
        "GSM-R",
        "IMT-A",
        "LTE",
        "LTE-A",
        "Mobil",
        "mobil",
        "Mobilní sítě",
        "mobilní sítě",
        "Mobilní síť",
        "Mobily",
        "P-P",
        "Pevné spoje",
        "pevný bezdrátový přístup",
        "pásmo 1800 MHz",
        "pásmo 800 MHz",
        "pásmo 900 MHz",
        "Přenos dat",
        "Přenos dat na společných kmitočtech",
        "Radio LAN",
        "RLAN",
        "terminály pro komunikaci pomocí družic",
        "UMTS",
        "UMTS FDD",
        "UMTS TDD",
        "WiFi",
        "Širokopásmový přenos dat",
    }

    OTHER = "0"
    DATA = "1"
    UNKNOWN = "2"

    pix_map = ""
    for f, k in freq_key_list:
        if not k or k == set([""]):
            pix_map += UNKNOWN
        elif data_keywords.intersection(k):
            pix_map += DATA
        else:
            pix_map += OTHER

    print render_sng(pix_map, 500, 1, 0)
    # print render_sng(pix_map, 50, 8, 10) # for cube visualisaition

    # Debug: uncoment to get list of all keywords
    # kwds = set()
    # for f, k in freq_key_list:
    #     kwds.update(k)

    # print "\n".join(kwds)
