import feedparser
import json

def test_link(rss_url):
    '''
    returns bool, True if rss_url is valid
    '''
    feed = feedparser.parse(rss_url)
    if feed:
        print(json.dumps(feed.feed))
        return True
    else:
        return False

# test_link('http://feeds.wired.com/wiredscience')

test_feed = feedparser.parse('https://news.ycombinator.com/rss')
keys = test_feed.keys()


for k in list(keys):
    print()
    print(k)
    feedk = test_feed[k]
    if k != 'bozo_exception':
        print(json.dumps(test_feed[k], indent=4))
    else:
        print(type(feedk))
    print()

print('feed keys:')
print(list(keys))

if 'feed' in keys:
    print('\nfeed.feed keys:')
    print(test_feed['feed'].keys())

print()
