import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

@raises(extract.HeaderWidthError)
def test_it_raises_error_when_first_row_is_not_widest_row():
    workbook, sheetNames = extract.extractExcel('fixture/temperature.xlsx')
    extract.validateHeaders(workbook[0])

@raises(extract.NullHeaderError)
def test_it_raises_error_when_first_row_contains_empty_cells():
    workbook, sheetNames = extract.extractCSV('fixture/empty-header-cells.csv')
    extract.validateHeaders(workbook[0])
