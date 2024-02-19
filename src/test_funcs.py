'''
Test Functions
'''

from .rss_tools import *

def test_func0():
    # temp test url = https://news.ycombinator.com/rss
    assert get_rss_feed()