import dash
from dash import Dash, callback_context, Input, Output, State, dcc, html, MATCH, ALL
import traceback
import openai
import os
from dash.exceptions import PreventUpdate

# custom libs
from rss_tools import *
from helpers import *

"""
Notes:
> API key: store as environ variable
"""

# Initialize Dash
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
server = app.server

# Global variable
# try:
#     API_KEY = os.environ['OPENAI_API_KEY']
# except:
#     API_KEY = None
# print(f'APIKEY: {API_KEY}')

# Use the function to read options from a file
options = read_options_from_file("../URLs/my_example_urls.txt")

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
                html.H5("or try example feeds from list:"),
                dcc.Dropdown(
                    id="rss-dropdown",
                    options=options,
                    style={
                        "margin-left": "10px",
                        "min-width": "25%",
                    },
                ),
            ],
        ),
        html.Div(
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-items": "center",
                "padding-top": "10px",
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
                id="loading-indicator-inner",
                type="circle",
                children=[html.Div(id="rss-json")],
            )
        ]
        # Update the output component with the loading indicator
        # output_div = html.Div(id='rss-output', children=children)
        # app.layout = html.Div([output_div])

        try:
            has_content, feed = get_rss_feed(url)
            if not has_content:
                return [
                    dcc.Markdown(
                        f"Bad Feed Error:\n{json.dumps(feed, indent=4)}",
                        style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
                    )
                ]

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
                            "Await connection to GPT",
                            id="refresh-button",
                            n_clicks=None,
                            style={
                                "color": "gray",
                            },
                        ),
                    ],
                ),
                html.Div(
                    id="gpt-input-div",
                    children=[],
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


# callback to summarize specific articles based on "SUMMARIZE" button click
@app.callback(
    Output({"type": "summarized-content", "index": MATCH}, "children"),
    Input({"type": "summarize-button", "index": MATCH}, "id"),
    Input({"type": "summarize-button", "index": MATCH}, "n_clicks"),
    Input("refresh-button", "disabled"),
)
def update_modal_children(btn_id, n_clicks, connected_to_gpt):
    if n_clicks is None:
        raise PreventUpdate

    # print(btn_id['index'])

    if connected_to_gpt:
        try:
            url = btn_id['index']
            summary = crawl_website(url)
            prompt = "Summarize this article in 150 words or less: " + summary
            gpt_summary = chat_with_gpt(prompt)
            return html.Div(
                gpt_summary,
                style={
                    "background-color": "rgba(128, 128, 128, 0.2)",
                    "padding": "20px",
                    "border-radius": "10px",
                    'margin-top': '10px',
                },
            ),
        except Exception as e:
            return [html.P(f"Error: {e}")]
    return "Not Connected to GPT"


@app.callback(
    Output("refresh-button", "style"),
    Output("refresh-button", "children"),
    Output("refresh-button", "disabled"),
    Output("refresh-button-note", "children"),
    Output("gpt-input-div", "children"),
    Input("refresh-button", "n_clicks"),
    State("api-key-input", "value"),
)
def refresh_connection(n_clicks, api_key):
    if n_clicks is not None:
        if openai.api_key is not None and valid_api_key(openai.api_key):
            return {"color": "green"}, "Connected to GPT", True, None, gpt_input_box()
        else:
            if api_key is not None and valid_api_key(api_key):
                openai.api_key = api_key
                return (
                    {"color": "green"},
                    "Connected to GPT",
                    True,
                    None,
                    gpt_input_box(),
                )
            else:
                try:
                    # default, set $OPENAI_API_KEY to PATH env variable
                    openai.api_key = os.environ["OPENAI_API_KEY"]
                    # print(openai.api_key)
                    if valid_api_key(openai.api_key):
                        return (
                            {"color": "green"},
                            "Connected to GPT",
                            True,
                            None,
                            gpt_input_box(),
                        )
                    else:
                        return (
                            {"color": "orange"},
                            "Not connected to GPT",
                            False,
                            [
                                "Please enter API key: ",
                                dcc.Input(id="api-key-input", type="text"),
                            ],
                            None,
                        )
                except:
                    return (
                        {"color": "orange"},
                        "Not connected to GPT",
                        False,
                        [
                            "Please enter API key: ",
                            dcc.Input(id="api-key-input", type="text"),
                        ],
                        None,
                    )
    else:
        return (
            {"color": "gray"},
            "Await connection to GPT",
            False,
            [
                "Please enter API key: ",
                dcc.Input(id="api-key-input", type="text"),
            ],
            None,
        )


@app.callback(
    Output("chat-output", "children"),
    Input("input-box", "n_submit"),
    State("input-box", "value"),
)
def ask_gpt(n_submit, value):
    if n_submit > 0:
        try:
            response = chat_with_gpt(value)
            return response
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
