import feedparser
import json

'''
Notes:
> pagination: feed size is rarely an issue
> custom URLs: you can generate at rss.app
'''

def get_rss_feed(rss_url):
    # Parse the RSS feed using feedparser
    feed = feedparser.parse(rss_url)
    
    print(f"\n>>> test printing feed for {rss_url}:")
    print(json.dumps(feed, indent=4))
    print(type(feed))
    print(feed.keys())

    feed_keys = feed.keys()

    # Extract the relevant feed data
    try:
        title = feed.feed.title
    except Exception as e:
        title = 'NA'
    try:
        link = feed.feed.link
    except Exception as e:
        link = 'NA'
    try:
        description = feed.feed.description
    except Exception as e:
        description = 'NA'

    # link = feed.feed.link
    # description = feed.feed.description
    entries = []
    try:
        for entry in feed.entries:
            entries.append({
                'title': entry.title,
                'link': entry.link,
                'description': entry.description,
                'published': entry.published,
            })
    except Exception as e:
        entries.append('sorry, invalid url')
    
    # Return feed data
    return {
        'title': title,
        'link': link,
        'description': description,
        'entries': entries,
    }

def valid_feed(url):
    try:
        fd = feedparser.parse(url)
        return True
    except:
        return False

# test
my_feed = get_rss_feed('http://rss.news.yahoo.com/rss/world')

print('\nFEED ENTRIES:')
print(json.dumps(list(my_feed['entries'])[-4:], indent=4))

