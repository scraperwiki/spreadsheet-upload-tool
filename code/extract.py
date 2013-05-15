#!/usr/bin/env python
# ScraperWiki Limited

"""Program to extract data from an Excel spreadsheet
and store it in a tabular database.
"""

import sys
import json
import csv

# http://www.lexicon.net/sjmachin/xlrd.html
import xlrd
# https://github.com/ahupp/python-magic
import magic
# https://github.com/scraperwiki/scraperwiki_local
import scraperwiki

Odict = dict
try:
    from collections import OrderedDict as Odict
except ImportError:
    pass


def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        filename = argv[1]
    if len(argv) != 2:
        raise ValueError("Please supply exactly one argument")
    save(extract(filename))


def detectType(filename):
    # detects the filetype of a given file
    # possible output values are: "xls", "xlsx", "csv", or other
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

def extract(filename, verbose=False):
    """Do something with a spreadsheet."""
    sheets = dict()
    if detectType(filename) in ['xls', 'xlsx']:
        book = xlrd.open_workbook(filename=filename, logfile=sys.stderr, verbosity=0)
        for sheetName in book.sheet_names():
            if verbose:
                print >>sys.stderr, "--- extracting sheet:", sheetName
            sheet = book.sheet_by_name(sheetName)
            validateHeaders(sheet)
            rows = list(sheetExtract(sheet, verbose))
            sheets[sheetName] = rows
    elif detectType(filename) == 'csv':
        with open(filename, 'r') as f:
            data = f.read()
            sheet = data.splitlines()
            validateHeaders(sheet)
            reader = csv.DictReader(sheet)
            rows = [convertRow(r) for r in reader]
            sheets['swdata'] = rows

    else:
        raise ValueError("Unknown file type (I only understand .csv, .xls and .xlsx)")

    return sheets


def save(sheets):
    for sheetName, rows in sheets.items():
        if rows:
            scraperwiki.sql.save([], rows, table_name=sheetName)


def sheetExtract(sheet, verbose=False):
    """Extract a table from the sheet (xlrd.Sheet)"""

    rows = sheet.nrows
    cols = sheet.ncols
    header = None
    for r in range(rows):
        row = [sheet.cell_value(r, c) for c in range(cols)]
        if verbose:
            print >>sys.stderr, "row:", row
        if all(x=='' for x in row):
            # if entire row is empty, skip to next row
            if verbose:
                print >>sys.stderr, "...skipping entirely empty row"
            continue
        if not header:
            # number of non-blank cells in row
            nonblank = sum(x!='' for x in row)
            if verbose:
                print >>sys.stderr, "...nonblank:", nonblank, "cols", cols
            if nonblank > 0.8*cols:
                if verbose:
                    print >>sys.stderr, "...non-blank greater than 90%, using as header"
                header = convertItemsToStrings(row)
            else:
                if verbose:
                    print >>sys.stderr, "...too many empty cells, not using as header"
        else:
            if verbose:
                print >>sys.stderr, "...using as body"
            zipped = zip(header, row)
            # ignore pairs with no header.
            d = Odict(((k,v) for k,v in zipped if k != ''))
            yield d


def convertItemsToStrings(row):
    # Turns items in the list "row" to strings.
    # Useful for avoiding column headers that are integers or floats.
    # return [ unicode(item) for item in row ]
    return row


def convertRow(row):
    return dict([(k, convertField(cell)) for k,cell in row.items()])


def convertField(string):
    types = [ (int, int), (float, float) ]
    for typ, test in types:
        try:
            return test(string)
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
