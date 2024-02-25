import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import feedparser
import json
from timeout import timeout
from collections import Counter
import openai


# 1. UI Helper Functions

# generate Card element from feed
def generate_feed(entries):
    children = []
    for entry in entries:
        '''
        display:
        - image if exists
        - title
        - description
        - link
        '''
        entry_fields = {
            "title": None,
            "link": None,
            "published": None,
            "summary": None,
            "content": None, # not yet implemented
            "media": None,
        }

        # must have title and link
        entry_fields['title'] = entry.get('title', 'No Title')
        entry_fields['link'] = entry.get('link', 'No Link')

        try:
            entry_fields['published'] = entry.get('published')
        except:
            entry_fields['published'] = 'No published date'

        try:
            entry_fields['summary'] = entry.get('summary')
        except:
            try:
                entry_fields['summary'] = entry.get('description')
            except:
                try:
                    entry_fields['summary'] = entry.get('content')
                except:
                    entry_fields['summary'] = 'No Summary'

        try:
            entry_fields['media'] = entry.get('media_content')
        except:
            entry_fields['media'] = None

        body_text = str(entry_fields['summary'])

        if '</' in body_text and '>' in body_text:
            body_text = (
                """<style>
                        img {
                            max-width:  100%;
                            height: auto;
                        }
                    </style>"""
                + body_text
            )
            card_description = html.Div(DangerouslySetInnerHTML(body_text))
        else:
            card_description = html.P(body_text, style={'white-space': 'pre-wrap', 'wordBreak': 'break-all'})

        card_body = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(entry['title']),
                    card_description,
                    dbc.CardLink("Go to source", href=entry['link']),
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
        if type(fd) == feedparser.FeedParserDict and not fd.bozo:
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

# 3. API Helper Functions

# check whether api key is valid
def valid_api_key(api_key):
    try:
        openai.api_key = api_key
        _models = openai.models.list()
        return True
    except:
        return False

# run as needed
if __name__=='__main__':
    # transfer_urls('../URLs/valid_url_list.txt', '../URLs/valid_urls_2.txt')

    print('now counting keys: ')
    key_counters = count_feed_keys( '../URLs/valid_urls_2.txt')
    print(json.dumps(key_counters, indent=4))
