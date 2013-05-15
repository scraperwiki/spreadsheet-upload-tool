#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

import sys
import json
import csv
import sys

# http://www.lexicon.net/sjmachin/xlrd.html
import xlrd
# https://github.com/ahupp/python-magic
import magic
# https://github.com/scraperwiki/scraperwiki_local
import scraperwiki

from collections import OrderedDict


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    if len(argv) != 2:
        raise ValueError("Please supply exactly one argument")
    save(extract(filename))


def extract(filename, verbose=False):
    """Convert a file into a list (workbook) of lists (sheets) of lists (rows)
    and then perform checks, and if all is ok, return dicts for saving to SQLite"""

    fileType = detectType(filename)
    if fileType not in ['xls', 'xlsx', 'csv']:
        raise ValueError("Unknown file type (I only understand .csv, .xls and .xlsx)")

    if fileType == 'csv':
        workbook, sheetNames = extractCSV(filename)
    else:
        workbook, sheetNames = extractExcel(filename)

    for sheet in workbook:
        validateHeaders(sheet)

    # sheets will be added to this dict,
    # as lists of dicts (rather than lists of lists)
    workbookForSQL = convertToOrderedDicts(workbook, sheetNames)

    for sheet in workbookForSQL:
        validateConsistency(sheet)

    return workbookForSQL


def detectType(filename):
    """Detects the filetype of a given file.
    Possible output values are: "xls", "xlsx", "csv", or something unexpected"""
    rawFileType = magic.from_file(filename)
    if rawFileType == 'ASCII text':
        return 'csv'
    elif rawFileType == 'Microsoft Excel 2007+':
        return 'xlsx'
    elif 'Excel' in rawFileType:
        return 'xls'
    elif 'Zip archive' in rawFileType and filename.endswith('.xlsx'):
        return 'xlsx'
    else:
        return rawFileType


def validateHeaders(rows):
    """Checks "rows" starts with a valid header row.
    rows should be a list of strings/integers/floats
    Will raise an error if:
    * the first row isn't the widest
    * the first row contains empty cells
    """
    pass


def validateConsistency(dictRows):
    """Checks each value in the list of dicts is of a consistent type"""
    pass


def extractExcel(filename):
    """Takes an excel file location, turns it into a
    list (workbook) of lists (sheets) of lists (rows)"""

    workbook = []
    sheetNames = []
    book = xlrd.open_workbook(filename=filename, logfile=sys.stderr, verbosity=0)

    for sheetName in book.sheet_names():
        sheetNames.append(sheetName)
        excelSheet = book.sheet_by_name(sheetName)
        nrows = excelSheet.nrows
        ncols = excelSheet.ncols
        sheet = []
        for r in range(nrows):
            row = [ excelSheet.cell_value(r, c) for c in range(ncols) ]
            sheet.append(row)
        workbook.append(sheet)

    return workbook, sheetNames


def extractCSV(filename):
    """Takes a csv file location, turns it into a
    list with one item which is a list (sheet) of lists (rows)"""

    workbook = []
    sheetNames = ['swdata']
    with open(filename, 'r') as f:
        sheet = []
        for row in csv.reader(f):
            typeConvertedRow = [ convertField(cell) for cell in row ]
            sheet.append(typeConvertedRow)
        workbook.append(sheet)

    return workbook, sheetNames


def convertToOrderedDicts(workbook, sheetNames):
    """Converts a list (workbook) of lists (sheets) of lists (rows) and
    a list of sheetNames, into a dict (workbookForSQL) of lists (sheets) of dicts (rows)"""
    workbookForSQL = OrderedDict()
    
    for sheet, sheetName in zip(workbook, sheetNames):
        sheetForSQL = []
        headers = sheet[0]
        for row in sheet[1:]:
            rowForSQL = OrderedDict( zip(headers, row) )
            sheetForSQL.append(rowForSQL)
        workbookForSQL[sheetName] = sheetForSQL

    return workbookForSQL


def save(sheets):
    for sheetName, rows in sheets.items():
        if rows:
            scraperwiki.sql.save([], rows, table_name=sheetName)


def convertField(string):
    types = [ int, float ]
    for t in types:
        try:
            return t(string)
        except ValueError:
            pass
    return string


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        # catch errors and wrap as JSON for frontend to display
        ret = {
            'error': str(e),
            'result': None
        }
        print json.dumps(ret)
    else:
        # return success as JSON for frontend to display
        ret = {
            'error': None,
            'result': "success"
        }
        print json.dumps(ret)
