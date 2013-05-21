import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

from collections import OrderedDict

import extract

def test_it_can_extract_a_simple_xls_file():
    sheets = extract.validate(extract.extract('fixture/simple.xls'))
    assert_equals(type(sheets), OrderedDict)
    assert_equals(len(sheets), 1)

    sheet = sheets['Sheet1']
    assert_equals(len(sheet), 4)
    row = sheet[2]
    assert_equals(row['Year'], 2012)
    assert_equals(row['Awesomeness'], 8)

def test_it_can_extract_a_simple_xlsx_file():
    sheets = extract.validate(extract.extract('fixture/simple.xlsx'))
    assert_equals(type(sheets), OrderedDict)
    assert_equals(len(sheets), 1)

    sheet = sheets['Sheet1']
    assert_equals(len(sheet), 4)
    row = sheet[2]
    assert_equals(row['Year'], 2012)
    assert_equals(row['Awesomeness'], 8)

def test_it_saves_to_the_database():
    sheets = extract.validate(extract.extract('fixture/simple.xlsx'))
    extract.save(sheets)

    data = scraperwiki.sql.select('* from Sheet1')
    row = data[2]
    assert_equals(row['Year'], 2012)
    assert_equals(row['Awesomeness'], 8)

def test_it_can_extract_a_simple_csv_file():
    sheets = extract.validate(extract.extract('fixture/simple.csv'))
    assert_equals(type(sheets), OrderedDict)
    assert_equals(len(sheets), 1)

    sheet = sheets['swdata']
    assert_equals(len(sheet), 4)
    row = sheet[2]
    assert_equals(row['Year'], 2012)
    assert_equals(row['Awesomeness'], 8)

