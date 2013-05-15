import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

@raises(TypeError)
def test_it_raises_error_when_first_row_is_not_widest_row():
    workbook, sheetNames = extract.extractExcel('fixture/temperature.xlsx')
    extract.validateHeaders(workbook[0])