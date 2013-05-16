import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

from collections import OrderedDict
import random

import extract

@raises(extract.ConsistencyError)
def test_it_raises_error_when_column_types_are_not_consistent():
    # construct a single-column table, with a "lat" column
    # which is 80% floats, 10% strings and 10% empty
    dictRows = []
    for i in range(80):
        row = OrderedDict([ ('lat', random.uniform(50.35, 58.56)) ])
        dictRows.append(row)
    for i in range(10):
        row = OrderedDict([ ('lat', 'fizz') ])
        dictRows.append(row)
    for i in range(10):
        row = OrderedDict([ ('lat', None) ])
        dictRows.append(row)

    extract.validateConsistency(dictRows)

def test_it_does_not_raise_error_when_column_types_are_consistent():
    # construct a single-column table, with a "lat" column
    # which is 60% floats, 40% empty
    dictRows = []
    for i in range(60):
        row = OrderedDict([ ('lat', random.uniform(50.35, 58.56)) ])
        dictRows.append(row)
    for i in range(40):
        row = OrderedDict([ ('lat', None) ])
        dictRows.append(row)

    extract.validateConsistency(dictRows)

def test_it_correctly_groups_together_integers_and_floats():
    # construct a single-column table, with a "lat" column which
    # which is 45% integers, 45% floats and 10% empty
    dictRows = []
    for i in range(45):
        row = OrderedDict([ ('lat', int(random.uniform(50.35, 58.56))) ])
        dictRows.append(row)
    for i in range(45):
        row = OrderedDict([ ('lat', random.uniform(50.35, 58.56)) ])
        dictRows.append(row)
    for i in range(10):
        row = OrderedDict([ ('lat', '') ])
        dictRows.append(row)

    extract.validateConsistency(dictRows)