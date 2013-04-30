import sys
sys.path.append('code')

from nose.tools import assert_equals

import extract

def test_it_attempts_to_extract_an_evil_xlsx_file():
    sheets = extract.extract('fixture/nhs-staff-2012.xlsx')
    assert_equals(type(sheets), dict)
    assert_equals(len(sheets), 6)

    sheet = sheets['Table 2a']
    assert len(sheet) >= 37
    row = sheet[2]
    assert_equals(len(row), 4) # 7 Columns
    assert_equals(row['Staff Group'], 'All HCHS doctors (incl locums)')
    assert_equals(row['12 month period ending March 2012'], 58226.66)



def test_it_correctly_detects_the_header_row_in_a_complicated_file():
    sheets = extract.extract('fixture/qep211.xls')

    sheet = sheets['Annual']
    assert_equals(sheet[0][u'ANNUAL FIGURES'], 1970)
