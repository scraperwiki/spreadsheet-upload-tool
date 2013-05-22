import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_an_xls_file():
    (filetype, encoding) = extract.detectType('fixture/simple.xls')
    assert_equals(filetype, 'excel')

def test_it_detects_an_xlsx_file():
    (filetype, encoding) = extract.detectType('fixture/simple.xlsx')
    assert_equals(filetype, 'excel')

def test_it_detects_a_csv_file():
    (filetype, encoding) = extract.detectType('fixture/simple.csv')
    assert_equals(filetype, 'csv')

def test_it_detects_a_random_file():
    (filetype, encoding) = extract.detectType('fixture/tractor.png')
    assert filetype not in ['csv', 'excel']

def test_it_detects_an_xlsx_file_that_shows_up_as_a_zip_archive_for_some_reason():
    (filetype, encoding) = extract.detectType('fixture/temperature.xlsx')
    assert_equals(filetype, 'excel')

def test_it_detects_a_csv_file_with_an_xls_extension():
    (filetype, encoding) = extract.detectType('fixture/really-a-csv.xls')
    assert_equals(filetype, 'csv')

def test_it_detects_an_xls_file_with_a_csv_extension():
    (filetype, encoding) = extract.detectType('fixture/really-an-xls.csv')
    assert_equals(filetype, 'excel')

def test_it_detects_a_random_file_with_a_csv_extension():
    (filetype, encoding) = extract.detectType('fixture/really-a-png.csv')
    assert filetype not in ['csv', 'excel']

@raises(extract.FileTypeError)
def test_it_raises_an_exception_for_unexpected_filetypes():
    extract.extract('fixture/tractor.png')