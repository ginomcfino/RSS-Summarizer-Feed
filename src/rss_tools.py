import feedparser
import json
import time
from timeout import timeout
import os

'''
Notes:
> pagination: feed size is rarely an issue
> custom URLs: you can generate at rss.app
'''

# helpers
@timeout(5)
def valid_feed(url):
    try:
        fd = feedparser.parse(url)
        if type(fd) == feedparser.FeedParserDict:
            return True
        else:
            return False
    except:
        return False
    
def load_json(filename):
    # Open the file
    with open(filename, 'r') as file:
        # Load the JSON data
        data = json.load(file)
        return data
    return None

def transfer_urls(txtfile, output=None):
    '''
    assume txtfile is a list of urls in utf-8 format
    '''
    if output:
        output = open(output, 'w') # convert output to writable file
    with open(txtfile, 'r') as file:
        for line in file:
            is_valid = valid_feed(line)
            print(str(f'{is_valid} {line}'), end='\r')
            if is_valid and output:
                if line.endswith('\n'):
                    output.write(line)
                else:
                    output.write(line + '\n')
    if output: output.close()



def get_rss_feed(rss_url):
    # Parse the RSS feed using feedparser
    feed = feedparser.parse(rss_url)
    
    print(f"\n>>> test printing feed for {rss_url}:")
    print(json.dumps(feed, indent=4))
    print(type(feed))

    print("\nKeys: ")
    print(feed.keys())
    print("Feed Keys: ")
    print(feed.feed.keys())
    print("Entries Keys: ")
    print(feed.entries[0].keys())

    feed_keys = feed.keys()

    feed_overall = {
        "title": None,
        "link": None,
        "subtitle" : None,
    }

    feed_entry = {
        "title": None,
        "published": None,
        "link": None,
        "desc": None,
    }

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
    

def test_get_rss(test_url):
    my_feed = get_rss_feed(test_url)
    print(my_feed)
    # print('\nFEED ENTRIES:')
    # print(json.dumps(list(my_feed['entries'])[-4:], indent=4))

def test_get_json():
    my_rss_list = load_json('../URLs/saved-urls.json')
    print(json.dumps(my_rss_list, indent=4))
    url_names = my_rss_list['URLs']
    test_url = my_rss_list['URLs']['Yahoo World News']
    print(test_url)

if __name__=='__main__':
    transfer_urls('../URLs/url_list.txt', '../URLs/valid_url_list.txt')
    

