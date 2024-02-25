import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import feedparser
import json
from timeout import timeout
from collections import Counter


# 1. UI Helper Functions

# generate Card element from feed
def generate_feed(feed):
    children = []
    for f in feed:
        '''
        display:
        - image if exists
        - title
        - description
        - link
        '''
        f = dict(f)
        body_text = f['description']
        if '<p>' in body_text:
            # use at own risk, make sure you trust the rss url
            card_description = DangerouslySetInnerHTML(body_text)
        else:
            card_description = html.P(body_text, style={'white-space': 'pre-wrap', 'wordBreak': 'break-all'})

        card_body = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(f['title']),
                    # html.P.Markdown(f['description']),
                    # html.P(f['description'], style={'white-space': 'pre-wrap', 'wordBreak': 'break-all'}),
                    card_description,
                    dbc.CardLink("Go to source", href=f['link']),
                ]
            ),
        )
        card = html.Div(
            style={
                "max-width": "60%",
                "margin": "30px auto",
                "padding": "20px",
                "text-align": "center",
                "border": "1px solid #ddd",
                "border-radius": "15px",
                "box-shadow": "2px 2px 2px lightgrey",
            },
            children=[card_body],
        )
        children.append(card)
    return children

# temporary fix (make dropdown options list from short input files)
def read_options_from_file(file_path):
    options = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove trailing newline
            options.append({"label": line, "value": line})
    return options

# 2. Data Helper Functions

# check if a feed url is valid
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

# load json from file
def load_json(filename):
    # Open the file
    with open(filename, 'r') as file:
        # Load the JSON data
        data = json.load(file)
        return data
    return None

# transfer valid urls from a file to another file
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

# count keys in a feed
def count_feed_keys(filename):
    '''
    filename: should lead to a text file with a list of urls
    '''
    feed_key_counter = Counter()
    entries_key_counter = Counter()
    feed_feed_key_counter = Counter()
    with open(filename, 'r') as file:
        for line in file:
            feed = feedparser.parse(line)
            feed_keys = list(feed.keys())
            try:
                entries_keys = list(feed.entries[0].keys())
            except:
                entries_keys = []
            try:
                feed_feed_keys = list(feed.feed.keys())
            except:
                feed_feed_keys = []
            # update_counter = lambda keys, counter: keys + counter
            update_counter(feed_keys, feed_key_counter)
            update_counter(entries_keys, entries_key_counter)
            update_counter(feed_feed_keys, feed_feed_key_counter)
    return {
        "feed": feed_key_counter,
        "entries": entries_key_counter,
        "feed feed": feed_feed_key_counter
    }

def update_counter(keys:list, counter:Counter):
    if len(keys) > 0:
        for k in keys:
            if k in counter:
                counter[k] += 1
            else:
                counter[k] = 1



# Test Scripts
# if __name__=='__main__':
#     # transfer_urls('../URLs/url_list.txt', '../URLs/valid_url_list.txt')
#     key_counters = count_feed_keys('../URLs/test_urls.txt')
#     print(json.dumps(key_counters, indent=4))