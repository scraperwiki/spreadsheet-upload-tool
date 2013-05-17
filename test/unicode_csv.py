# -*- coding: utf-8 -*-

import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_unicode_csv_file():
    filetype = extract.detectType('fixture/mps_unicode.csv')
    assert_equals(filetype, 'csv')


def test_it_can_extract_a_unicode_csv():
    sheets = extract.extract('fixture/mps_unicode.csv')
    assert_equals(len(sheets), 1)

    sheet = sheets['swdata']
    assert_equals(len(sheet), 653)
    row = sheet[460]
    assert_equals(row['MP Name'], 'Michelle Gildernew')
    assert_equals(row['Party'], u'Sinn Féin')
    

def test_it_saves_a_unicode_csv_to_the_database():
    sheets = extract.extract('fixture/mps_unicode.csv')
    extract.save(sheets)

    data = scraperwiki.sql.select('* from swdata')
    row = data[460]
    assert_equals(row['MP Name'], 'Michelle Gildernew')
    assert_equals(row['Party'], u'Sinn Féin')