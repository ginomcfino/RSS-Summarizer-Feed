from helpers import *

'''
Notes:
> pagination: feed size is rarely an issue
> custom URLs: you can generate at rss.app
'''
            


def get_rss_feed(rss_url):
    '''
    returns a dictionary if the feed is valid, otherwise returns None
    '''
    # Parse the RSS feed using feedparser
    feed = feedparser.parse(rss_url)

    # try:
    #     print(f"\n>>> test printing feed for {rss_url}:")
    #     # print(json.dumps(feed, indent=4))
    #     print(type(feed))

    #     print("Keys: ")
    #     print(feed.keys())
    #     print("Feed Keys: ")
    #     print(feed.feed.keys())
    #     print("Entries Keys: ")
    #     print(feed.entries[0].keys())
    # except Exception as e:
    #     print(f'\nError Printing: {e}')

    if feed.bozo:
        return 'Bozo Error'
    else:
        return feed
    
    # common feed elements:
    




    # feed_keys = feed.keys()

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

# if __name__=='__main__':
#     # transfer_urls('../URLs/url_list.txt', '../URLs/valid_url_list.txt')
#     key_counters = count_feed_keys('../URLs/test_urls.txt')
#     print(json.dumps(key_counters, indent=4))
    

