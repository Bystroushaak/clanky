#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple

import dhtmlparser  # pip install -U dhtmlparser
from httpkie import Downloader  # pip install -U httpkie


# Variables ===================================================================
downloader = Downloader()
MIPSInfo = namedtuple("MIPSInfo", "name mips year")


# Functions & classes =========================================================
def get_table():
    page = downloader.download(
        "https://en.wikipedia.org/wiki/Instructions_per_second"
    )

    dom = dhtmlparser.parseString(page)

    return dom.find("table", {"class": "wikitable sortable"})[0]


def parse_table():
    for tr in get_table().find("tr"):
        tds = tr.find("td")

        if not tds:
            continue

        name = dhtmlparser.removeTags(tds[0])
        mips = dhtmlparser.removeTags(tds[1])
        year = dhtmlparser.removeTags(tds[4])

        # clean mips
        mips = mips.replace("&#160;", " ")
        mips = mips.split("MIPS")[0].replace(",", "").strip()

        yield MIPSInfo(name, float(mips), int(year))


# Main program ================================================================
if __name__ == '__main__':
    # parsed = list(parse_table())
    # x_vals = [item.year for item in parsed]
    # y_vals = [item.mips for item in parsed]

    print "\n".join(
        "; ".join(str(x) for x in item)
        for item in parse_table()
    )
