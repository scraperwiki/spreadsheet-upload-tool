import sys
sys.path.append('code')

from nose.tools import assert_equals
import scraperwiki

import xlextract

def test_it_can_extract_an_evil_xlsx_file():
    sheets = xlextract.extract('fixture/nhs-staff-2012.xlsx')
    assert_equals(type(sheets), dict)
    assert_equals(len(sheets), 6)

    sheet = sheets['Table 2a']
    assert_equals(len(sheet), 37)
    row = sheet[2]
    assert_equals(len(row), 4) # 7 Columns
    assert_equals(row['Staff Group'], 'All HCHS doctors (incl locums)')
    assert_equals(row['12 month period ending March 2013'], 578226.66)

