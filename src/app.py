import dash
from dash import Input, Output, State, dcc, html
import traceback
import openai
import os
# custom libs
from rss_tools import *
from helpers import *

'''
Notes:
> API key: store as environ variable
'''

# Initialize Dash
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# Global variable
# try:
#     API_KEY = os.environ['OPENAI_API_KEY']
# except:
#     API_KEY = None
# print(f'APIKEY: {API_KEY}')

# Use the function to read options from a file
options = read_options_from_file('../URLs/my_example_urls.txt')

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
                html.H1("RSS feed dashboard"),
                html.P(
                    "project repository: https://github.com/ginomcfino/RSS-Summarizer-Feed"
                ),
                html.Br(),
                html.H4("enter rss feed url:"),
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
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
            children=[
                html.H5("or select from the list:"),
                dcc.Dropdown(
                    id="rss-dropdown",
                    options=options,
                    style={
                        'margin-left': '10px',
                        'min-width': '25%',
                    }
                ),
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
    Output("rss-input", "value"),
    Input("rss-dropdown", "value"),
)
def update_input(value):
    if value is not None:
        return value

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
        # output_div = html.Div(id='rss-output', children=children)
        # app.layout = html.Div([output_div])

        try:
            has_content, feed = get_rss_feed(url)
            if not has_content:
                return [dcc.Markdown(f"Bad Feed Error:\n{json.dumps(feed, indent=4)}", style={'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'})]

            # otherwise, feed has valid list of entries, convert them to cards
            children = [
                html.Div(
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                    children=[
                        html.Div(
                            id="refresh-button-note",
                            style={
                                "padding-left": "10px",
                                "padding-right": "10px",
                            },
                            children=[
                                "Please enter API key: ",
                                dcc.Input(id="api-key-input", type="text"),
                            ],
                        ),
                        html.Button(
                            "Await GPT Connection",
                            id="refresh-button",
                            n_clicks=0,
                            style={
                                "color": "orange",
                            },
                        ),
                    ],
                ),
            ]

            children += generate_feed(feed)

            # Set the loading indicator to False
            # children_inner = [html.Div(id="rss-json")]
            # output_div_inner = html.Div(id='rss-output', children=children_inner)
            # app.layout = html.Div([output_div_inner])

            return children
        except Exception as e:
            print(traceback())
            print()
            print(e)
            return [html.P(f"Error: {e}")]

@app.callback(
    Output("refresh-button", "style"),
    Output("refresh-button", "children"),
    Output("refresh-button-note", "children"),
    Input("refresh-button", "n_clicks"),
    State("api-key-input", "value"),
)
def refresh_connection(n_clicks, api_key):
    if n_clicks is not None:
        if openai.api_key is not None and valid_api_key(openai.api_key):
            return {"color": "green"}, "Connected to GPT", None
        else:
            if api_key is not None and valid_api_key(api_key):
                openai.api_key = api_key
                return {"color": "green"}, "Connected to GPT", None
            else:
                try:
                    # default, set $OPENAI_API_KEY to PATH env variable
                    openai.api_key = os.environ['OPENAI_API_KEY']
                    # print(openai.api_key)
                    if valid_api_key(openai.api_key):
                        return {"color": "green"}, "Connected to GPT", None
                    else:
                        return (
                            {"color": "red"},
                            "Not connected to GPT",
                            [
                                "Please enter API key: ",
                                dcc.Input(id="api-key-input", type="text"),
                            ],
                        )
                except:
                    return (
                        {"color": "red"},
                        "Not connected to GPT",
                        [
                            "Please enter API key: ",
                            dcc.Input(id="api-key-input", type="text"),
                        ],
                    )
    # else:
    #     return (
    #         {"color": "orange"},
    #         "Await connction to GPT",
    #         [
    #             "Please enter API key: ",
    #             dcc.Input(id="api-key-input", type="text"),
    #         ],
    #     )

if __name__ == "__main__":
    app.run_server(debug=True)

    # for prod:
    # application.debug = True
    # application.run(port=80)
