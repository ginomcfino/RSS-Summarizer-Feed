import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import feedparser
import json
from timeout import timeout
from collections import Counter
import openai
import datetime
import requests
from bs4 import BeautifulSoup


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

        if '<' in body_text and '>' in body_text:
            body_text = (
                """<style>
                        img {
                            max-width:  100%;
                            height: auto;
                        }
                    </style>"""
                + body_text
            )
            card_description = html.Div(DangerouslySetInnerHTML(body_text), style={'white-space': 'pre-wrap', 'wordBreak': 'break-all'})
        else:
            card_description = html.P(body_text, style={'white-space': 'pre-wrap', 'wordBreak': 'break-all'})

        card = dbc.Card(
            children=[
                dbc.CardHeader(
                    html.H4(
                        entry["title"],
                        style={"text-align": "center", "text-justify": "inter-word"},
                    )
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            card_description,
                            style={
                                "background-color": "rgba(128, 128, 128, 0.2)",
                                "padding": "20px",
                                "border-radius": "10px",
                            },
                        ),
                        html.Div(
                            style={"text-align": "center"},
                            children=[
                                html.Small(f"Published: {convert_timestamp(entry_fields['published'])}"),
                                html.Div(style={"height": "10px"}),
                                dbc.CardLink("view article", href=entry["link"]),
                            ],
                        ),
                    ]
                ),
                dbc.CardFooter(
                    [
                        html.Div(
                            children=[
                                dbc.Button(
                                    "Summarize",
                                    color="primary",
                                    className="mr-1",
                                    id={
                                        'type': "summarize-button",
                                        'index': f"{entry_fields['link']}",
                                    },
                                ),
                                html.Div(
                                    id={
                                        'type': "summarized-content",
                                        'index': f"{entry_fields['link']}",
                                    },
                                    style={"text-align": "left"},
                                ),
                            ],
                            style={"text-align": "center"},
                        ),
                    ]
                ),
            ],
            style={
                "max-width": "80%",
                "margin": "auto",
                "padding-left": "10px",
                "padding-right": "10px",
                "padding-bottom": "10px",
                "border": "1px solid #ddd",
                "border-radius": "15px",
                "box-shadow": "2px 2px 2px lightgrey",
            },
        )
        card_div = html.Div(
            style={
                "padding": "20px",
                "align-items": "center",
            },
            children=[card],
        )
        children.append(card_div)
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

def convert_timestamp(timestamp_str):
    try:
        timestamp = datetime.datetime.strptime(timestamp_str, '%a, %d %b %Y %H:%M:%S %z')
        return timestamp.strftime('%a, %d %b %Y %H:%M:%S')
    except:
        return timestamp_str
    
# craw website to return content as text ata
def crawl_website(url):
    response = requests.get(url)
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      data = [p.get_text() for p in soup.find_all('p')]
      # Changing data to a single string
      return ' '.join(data)
    else:
      return(f"Failed to crawl {url}. code {response.status_code}")

# 3. API Helper Functions

# check whether api key is valid
def valid_api_key(api_key):
    try:
        openai.api_key = api_key
        _models = openai.models.list()
        return True
    except:
        return False
    
# TODO: make funtions to select different models from OpenAI, Anthropic, and others.
def chat_with_gpt(user_input, model_name="gpt-3.5-turbo"):
    """
    Sends a message to the GPT model and returns the model's response.
    """
    completion = openai.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
        ],
    )
    return completion.choices[0].message.content


def gpt_input_box():
    return html.Div(
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "justify-content": "center",
                    "align-items": "center",
                },
                children=[
                    html.Div(
                        style={
                            "padding-left": "20px",
                            "padding-top": "10px",
                        },
                        children=[
                            dcc.Input(
                                id="input-box",
                                type="text",
                                n_submit=0,
                                placeholder="chat...",
                                style={
                                    "width": "550px",
                                },
                            ),
                        ],
                    )
                ],
            ),
            html.Div(
                # id="gpt-output",
                children=[
                    dcc.Loading(
                        # id="loading-1",
                        type="default",  # You can change this to "circle", "cube", etc.
                        children=[
                            dcc.Markdown(
                                id="chat-output", loading_state={"is_loading": True}
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

# run as needed
if __name__=='__main__':
    # transfer_urls('../URLs/valid_url_list.txt', '../URLs/valid_urls_2.txt')

    print('now counting keys: ')
    key_counters = count_feed_keys( '../URLs/valid_urls_2.txt')
    print(json.dumps(key_counters, indent=4))
