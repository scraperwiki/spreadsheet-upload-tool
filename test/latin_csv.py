# -*- coding: utf-8 -*-

import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_a_latin1_csv_file():
    (filetype, encoding) = extract.detectType('fixture/ENH-CCG-spend-2013.csv')
    assert_equals(filetype, 'csv')
    assert_equals(encoding, 'latin-1')


def test_it_can_extract_a_latin1_csv():
    sheets = extract.validate(extract.extract('fixture/ENH-CCG-spend-2013.csv'))
    assert_equals(len(sheets), 1)

    row = sheets['swdata'][1]
    assert_equals(row['Purchase invoice number'], 11223)
