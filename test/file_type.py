import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_an_xls_file():
    filetype = extract.detectType('fixture/simple.xls')
    assert_equals(filetype, 'xls')

def test_it_detects_an_xlsx_file():
    filetype = extract.detectType('fixture/simple.xlsx')
    assert_equals(filetype, 'xlsx')

def test_it_detects_a_csv_file():
    filetype = extract.detectType('fixture/simple.csv')
    assert_equals(filetype, 'csv')

def test_it_detects_a_random_file():
    filetype = extract.detectType('fixture/tractor.png')
    assert filetype not in ['csv', 'xls', 'xlsx']

def test_it_detects_a_csv_file_with_an_xls_extension():
    filetype = extract.detectType('fixture/really-a-csv.xls')
    assert_equals(filetype, 'csv')

def test_it_detects_an_xls_file_with_a_csv_extension():
    filetype = extract.detectType('fixture/really-an-xls.csv')
    assert_equals(filetype, 'xls')

def test_it_detects_a_random_file_with_a_csv_extension():
    filetype = extract.detectType('fixture/really-a-png.csv')
    assert filetype not in ['csv', 'xls', 'xlsx']
