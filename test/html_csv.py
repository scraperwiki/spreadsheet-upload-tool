# -*- coding: utf-8 -*-

import sys
sys.path.append('code')

from nose.tools import *
import scraperwiki

import extract

def test_it_detects_an_html_csv_file():
    (filetype, encoding) = extract.detectType('fixture/twitter-archive.csv')
    assert_equals(filetype, 'csv')
    assert_equals(encoding, 'ascii')


def test_it_can_extract_an_html_csv():
    sheets = extract.validate(extract.extract('fixture/twitter-archive.csv'))
    assert_equals(len(sheets), 1)

    row = sheets['swdata'][3]
    assert_equals(row['source'], '<a href="http://www.tweetdeck.com" rel="nofollow">TweetDeck</a>')
