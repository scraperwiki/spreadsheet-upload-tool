import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_ignores_empty_workbook_sheets():
    workbook, sheetNames = extract.extract('fixture/british-wars.xlsx')
    assert_equals(type(workbook), list)
    assert_equals(len(workbook), 1)
