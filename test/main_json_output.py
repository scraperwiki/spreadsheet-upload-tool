import sys
import json
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_returns_success_json():
    rawOutput = extract.main(['./extract.py','fixture/simple.xls'])
    output = json.loads(rawOutput)
    assert("errorType" in output)
    assert_equals(output["errorType"],None)
    
def test_it_returns_error_json():
    rawOutput = extract.main(['./extract.py','fixture/empty-header-cells.csv'])
    output = json.loads(rawOutput)
    assert("errorType" in output)
    assert_equals(output["errorType"],"NullHeaderError")