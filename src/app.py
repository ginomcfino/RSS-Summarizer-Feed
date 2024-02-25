import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import os
import openai
import traceback
import time
# custom library
from rss_tools import *
from helpers import *

'''
Notes:
> API key: store as environ variable
'''

# Initialize Dash
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Global variable
# try:
#     API_KEY = os.environ['OPENAI_API_KEY']
# except:
#     API_KEY = None
# print(f'APIKEY: {API_KEY}')

# Use the function to read options from a file
options = read_options_from_file('../URLs/test_urls.txt')

# Define layout
app.layout = html.Div(
    [
        html.Div(
            # style={"display": "flex", "justify-content": "center", "gap": "10px"},
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
            },
            children=[
                html.H1("RSS feed dashboard wih GPT"),
                html.P(
                    "project repository: https://github.com/ginomcfino/RSS-Summarizer-Feed"
                ),
                html.H4("input rss feed url:"),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
            children=[
                dcc.Input(
                    id="rss-input",
                    type="text",
                    placeholder="ex: https://news.ycombinator.com/rss",
                    style={"width": "50%"},
                    n_submit=0,
                ),
                html.Button("Submit", id="rss-submit", n_clicks=0),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                'padding-top': '10px',
            },
            children=[
                dcc.Loading(
                    id="loading-indicator",
                    type="circle",
                    children=[html.Div(id="rss-output")],
                ),
            ],
        ),
    ]
)

@app.callback(
    Output("rss-output", "children"),
    Input("rss-submit", "n_clicks"),
    Input("rss-input", "n_submit"),
    State("rss-input", "value"),
)
def update_output(n_clicks_submit, n_clicks_input, url):
    if n_clicks_submit > 0 or n_clicks_input > 0:
        # Set the loading indicator to True
        children = [
            dcc.Loading(
                id='loading-indicator-inner',
                type='circle',
                children=[
                    html.Div(id='rss-json')
                ],
            )
        ]
        # Update the output component with the loading indicator
        output_div = html.Div(id='rss-output', children=children)
        app.layout = html.Div([output_div])

        try:
            feed = get_rss_feed(url)
            feed_json = json.dumps(feed, indent=4)
            print(feed_json)
            children = [
                dcc.Markdown(feed_json, style={'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'}, id='rss-json'),
            ]
            # Set the loading indicator to False
            children_inner = [
                html.Div(id='rss-json')
            ]
            output_div_inner = html.Div(id='rss-output', children=children_inner)
            app.layout = html.Div([output_div_inner])
            return children
        except Exception as e:
            print(traceback())
            print()
            print(e)
            return [html.P(f"Error: {e}")]

if __name__ == "__main__":
    app.run_server(debug=True)

    # for prod:
    # application.debug = True
    # application.run(port=80)
