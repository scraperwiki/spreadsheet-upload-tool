import sys, os
sys.path.append('code')

from nose.tools import *
import scraperwiki

from collections import OrderedDict

import extract

def test_it_clears_the_database_when_reuploading_a_file():
    extract.main(['./extract.py', 'fixture/simple.xlsx'])

    extract.main(['./extract.py', 'fixture/mps.xlsx'])

    sheet1 = scraperwiki.sql.select('count(*) as n from Sheet1')
    assert_equals(sheet1[0]['n'], 308)

    sheet2 = scraperwiki.sql.select('count(*) as n from Sheet2')
    assert_equals(sheet2[0]['n'], 1073)
