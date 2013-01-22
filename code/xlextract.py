#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

# http://www.lexicon.net/sjmachin/xlrd.html
import xlrd

def extract(filename):
    """Do somethng with an Excel spreadsheet."""

    # :todo: consider providing encoding_override feature.
    book = xlrd.open_workbook(filename=filename)
    for sheetName in book.sheet_names():
      sheet = book.sheet_by_name(sheetName)
      sheetExtract(sheet)

def sheetExtract(sheet):
    """Do something with a sheet (xlrd.Sheet) from an
    Excel spreadsheet."""

    print "Extracting %r ..." % sheet.name
    rows = sheet.nrows
    cols = sheet.ncols
    print "%r cols by %r rows" % (cols, rows)
    for r in range(rows):
        print [sheet.cell_value(r, c) for c in range(cols)]


def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    extract(filename)

if __name__ == '__main__':
  main()
