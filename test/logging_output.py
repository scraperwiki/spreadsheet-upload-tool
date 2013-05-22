import sys
import json
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_logs_progress_to_a_text_file():
    extract.main(['./extract.py','fixture/simple.xls'])
    with open('log.txt', 'r') as f:
        assert("STARTED" in f.read())

def test_it_clears_the_log_before_each_run():
    extract.main(['./extract.py','fixture/simple.xls'])
    with open('log.txt', 'r') as f:
        assert_equals(f.read().count('STARTED'), 1)

def test_it_logs_stack_traces():
    extract.main(['./extract.py','fixture/empty-header-cells.csv'])
    with open('log.txt', 'r') as f:
        logOutput = f.read()
        assert('Traceback (most recent call last):' in logOutput)
        assert('NullHeaderError' in logOutput)