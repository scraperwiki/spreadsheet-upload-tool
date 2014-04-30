#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

import sys
import json
import datetime
import traceback
from collections import OrderedDict, Counter

# http://www.lexicon.net/sjmachin/xlrd.html
import xlrd
# https://github.com/ahupp/python-magic
import magic
# https://github.com/scraperwiki/scraperwiki_local
import scraperwiki
# https://pypi.python.org/pypi/unicodecsv/
import unicodecsv

LOGFILE = 'log.txt'

class HeaderWidthError(Exception):
    pass


class NullHeaderError(Exception):
    pass


class FileTypeError(Exception):
    pass


def main(argv=None):
    log('STARTED', True)
    try:
        if argv is None:
            argv = sys.argv
        if len(argv) > 1:
            filename = argv[1]
        if len(argv) != 2:
            log("EXCEPTION\nValue Error: Please supply exactly one argument")
            raise ValueError("Please supply exactly one argument")
        save(validate(extract(filename)))

    except Exception, e:
        # catch errors and wrap as JSON for frontend to display
        ret = {
            'errorType': type(e).__name__,
            'errorMessage': str(e)
        }
        log('EXCEPTION')
        traceback.print_exc(file=open(LOGFILE,'a'))
        return json.dumps(ret)

    else:
        # return success as JSON for frontend to display
        ret = {
            'errorType': None,
            'errorMessage': None
        }
        log('COMPLETED')
        return json.dumps(ret)


def extract(filename, verbose=False):
    """Convert a file into a list (workbook) of lists (sheets) of lists (rows)"""

    log("Extracting file: %s" % filename)

    (fileType, encoding) = detectType(filename)

    if fileType == 'csv':
        log("Filetype: CSV (%s)" % encoding)
        workbook, sheetNames = extractCSV(filename, encoding)
    elif fileType == 'excel':
        log("Filetype: Excel")
        workbook, sheetNames = extractExcel(filename)
    else:
        raise FileTypeError("Unknown file type <b>%s</b> (I only understand .csv, .xls and .xlsx)" % fileType)

    return (workbook, sheetNames)


def validate(output_from_extract):
    """perform checks on output of extract(), and if all is ok, return dicts for saving to SQLite"""

    log('Validating extracted data')

    workbook, sheetNames = output_from_extract

    for sheet in workbook:
        validateHeaders(sheet)

    # sheets will be added to this dict,
    # as lists of dicts (rather than lists of lists)
    workbookForSQL = convertToOrderedDicts(workbook, sheetNames)

    return workbookForSQL


def detectType(filename):
    """Detects the filetype of a given file. Excel, CSV, or anything else."""
    rawFileType = magic.from_file(filename)
    rawMimeType = magic.from_file(filename, mime=True)
    if rawMimeType in ['text/plain', 'text/html']:
        if 'UTF-8 Unicode' in rawFileType:
            return ('csv', 'utf-8')
        elif 'ISO-8859' in rawFileType:
            return ('csv', 'latin-1')
        else:
            return ('csv', 'ascii')
    elif 'application/vnd.ms-excel' in rawMimeType:
        return ('excel', None)
    elif rawMimeType == 'application/zip' and filename.endswith('xlsx'):
        return ('excel', None)
    else:
        return (rawFileType, None)


def validateHeaders(rows):
    """Checks "rows" starts with a valid header row.
    rows should be a list of strings/integers/floats
    Will raise an error if:
    * the first row isn't the widest
    * the first row contains empty cells
    """
    maxRowLength = max(map(len, rows[1:]))
    if len(rows[0]) < maxRowLength:
        raise HeaderWidthError("Your header row isn't the widest in the table")

    if None in rows[0] or "" in rows[0]:
        raise NullHeaderError("Your header row contains empty cells")


def extractExcel(filename):
    """Takes an excel file location, turns it into a
    list (workbook) of lists (sheets) of lists (rows)"""

    workbook = []
    sheetNames = []
    book = xlrd.open_workbook(filename=filename, ragged_rows=True, logfile=sys.stderr, verbosity=0)

    for sheetName in book.sheet_names():
        sheetNames.append(sheetName)
        excelSheet = book.sheet_by_name(sheetName)
        nrows = excelSheet.nrows
        sheet = []
        if nrows > 0:
            for rowx in range(nrows):
                row = excelSheet.row_values(rowx)
                sheet.append(row)
            workbook.append(sheet)

    return workbook, sheetNames


def extractCSV(filename, encoding):
    """Takes a csv file location, turns it into a
    list with one item which is a list (sheet) of lists (rows)"""

    workbook = []
    sheetNames = ['swdata']
    with open(filename, 'r') as f:
        sheet = []
        # we could use strict=True here too but may produce too many errors
        for row in unicodecsv.reader(f, encoding=encoding, skipinitialspace=True):
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
    log("Saving %s sheet%s" % (len(sheets), 's' if len(sheets) != 1 else ''))
    tables = scraperwiki.sql.show_tables()
    for table in tables.keys():
        scraperwiki.sql.execute('drop table "%s"' % table)
        scraperwiki.sql.commit()
    for sheetName, rows in sheets.items():
        if rows:
            scraperwiki.sql.save([], rows, table_name=sheetName)


def convertField(string):
    types = [ int, float ]
    for t in types:
        try:
            return t(string.replace(',', ''))
        except ValueError:
            pass
    return string


def humanType(thing):
    t = type(thing).__name__
    types = {
        "int": "number",
        "float": "number",
        "long": "number",
        "NoneType": "empty",
        "str": "string",
        "unicode": "string"
    }
    if thing == '':
        return "empty"
    elif t in types:
        return types[t]
    else:
        return t


def log(message, newfile=False):
    if newfile:
        method = 'w'
    else:
        method = 'a'
    with open(LOGFILE, method) as f:
        f.write("%s %s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))


if __name__ == '__main__':
    print main()
    
