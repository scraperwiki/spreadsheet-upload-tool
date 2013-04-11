import sys
sys.path.append('code')

from nose.tools import assert_equals

import extract

def test_it_can_extract_a_tricky_xls_file():
    sheets = extract.extract('fixture/deprivation-2010.xls')
    assert_equals(type(sheets), dict)
    assert_equals(len(sheets), 2) # TODO: this should be 1

    sheet = sheets['IMD 2010']
    assert_equals(len(sheet), 32482)
    row = sheet[6514 - 2] # excel row 6514, but we strip headers and 0-index
    assert_equals(len(row), 7) # 7 Columns
    assert_equals(row['LSOA CODE'], 'E01006513')
    assert_equals(row['IMD SCORE'], 22.88577)
    assert_equals(row['RANK OF IMD SCORE (where 1 is most deprived)'], 11973)

