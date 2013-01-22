#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

import xlrd

def extract(filename):
    """Do somethng with an Excel spreadsheet."""

    # :todo: consider providing encoding_override feature.
    book = xlrd.open_workbook(filename=filename)
    for sheetName in book.sheet_names():
      print sheetName

def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    extract(filename)

if __name__ == '__main__':
  main()
