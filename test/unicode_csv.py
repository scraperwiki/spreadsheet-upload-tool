import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_unicode_csv_file():
    filetype = extract.detectType('fixture/mps_unicode.csv')
    assert_equals(filetype, 'csv')
