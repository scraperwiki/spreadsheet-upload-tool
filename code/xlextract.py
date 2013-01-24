#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

import sys

# http://www.lexicon.net/sjmachin/xlrd.html
import xlrd
# https://github.com/scraperwiki/scraperwiki_local
import scraperwiki

Odict = dict
try:
    from collections import OrderedDict as Odict
except ImportError:
    pass

def extract(filename):
    """Do something with an Excel spreadsheet."""

    sheets = dict()
    # :todo: consider providing encoding_override feature.
    book = xlrd.open_workbook(filename=filename)
    for sheetName in book.sheet_names():
        sheet = book.sheet_by_name(sheetName)
        rows = list(sheetExtract(sheet))
        sheets[sheetName] = rows
    return sheets

def save(sheets):
    for sheetName, rows in sheets.items():
        scraperwiki.sqlite.save([], rows, table_name=sheetName)

def sheetExtract(sheet):
    """Extract a table from the sheet (xlrd.Sheet) and store it
    in a sqlite database using the scraperwiki module.

    There are all sorts of complicated things to do with which
    rectangular section it extracts for the table, and what the
    headers end up being.
    """

    rows = sheet.nrows
    cols = sheet.ncols
    header = None
    for r in range(rows):
        row = [sheet.cell_value(r, c) for c in range(cols)]
        if all(x=='' for x in row):
            # if entire row is empty, skip to next row
            continue
        if not header:
            # number of non-blank cells in row
            nonblank = sum(x!='' for x in row)
            if nonblank > 0.9*cols:
                header = row
        else:
            zipped = zip(header, row)
            # ignore pairs with no header.
            d = Odict(((k,v) for k,v in zipped if k != ''))
            yield d


def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    if len(argv) != 2:
        print >> sys.stderr, "Please supply exactly one argument"
    save(extract(filename))

if __name__ == '__main__':
  main()
