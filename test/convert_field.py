import sys
sys.path.append('code')

from nose.tools import *

import extract

def test_it_converts_a_int_string_to_an_int():
    assert_equals(extract.convertField('10'), 10)

def test_it_converts_a_float_string_to_an_float():
    assert_equals(extract.convertField('10.232'), 10.232)

def test_it_converts_a_string_to_a_string():
    assert_equals(extract.convertField('foo'), 'foo')

def test_it_converts_an_int_with_commas_to_an_int():
    assert_equals(extract.convertField('1,234'), 1234)

def test_it_converts_a_float_with_commas_to_a_float():
    assert_equals(extract.convertField('1,234.56'), 1234.56)
