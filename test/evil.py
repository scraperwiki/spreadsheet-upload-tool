import sys
sys.path.append('code')
import os

from nose.tools import assert_equals

import extract

import scraperwiki

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


# This fails - will be changed with card PICKY UPLOAD SPREADSHEET TOOL
# def test_it_correctly_detects_the_header_row_in_a_complicated_file():
#     sheets = extract.extract('fixture/qep211.xls', verbose=False)
# 
#     assert_equals(sheets['Annual'][0][u'ANNUAL FIGURES'], 1970)
#     assert_equals(sheets['Quarterly'][0][u'QUARTERLY FIGURES'], 1970)
#     
#     tmpname = "/tmp/spreadsheet-upload-tool-evil-test.sqlite"
#     if os.path.isfile(tmpname):
#         os.remove(tmpname)
#     scraperwiki.sqlite._connect(tmpname)
#     extract.save(sheets)

