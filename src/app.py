import dash
from dash import Input, Output, State, dcc, html
import dash_bootstrap_components as dbc
import os
import openai
# custom library
from rss_tools import *
import traceback

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
#     # API_KEY = os.environ['Does not esixt']
# except:
#     API_KEY = None
# print(f'APIKEY: {API_KEY}')

# Define layout
app.layout = html.Div(
    [
        html.Div(
            # style={"display": "flex", "justify-content": "center", "gap": "10px"},
            style={"text-align": "center"},
            children=[
                html.H1("RSS feed dashboard wih GPT"),
                # dcc.Input(
                #     id="saved-api-key",
                #     type="password",
                #     placeholder="API key missing...",
                # ),
                # html.Button("Submit", id="api-key-submit", n_clicks=0),
                html.Div("select feed"),
                dcc.Input(
                    id="rss-input",
                    type="text",
                    placeholder="https://news.ycombinator.com/rss",
                    style={"width": "50%"},
                ),
                # dcc.Dropdown(
                #     id="rss-input",
                #     options=[
                #         {"label": "Option 1", "value": "1"},
                #         {"label": "Option 2", "value": "2"},
                #         {"label": "Option 3", "value": "3"},
                #     ],
                #     searchable=True,
                #     placeholder="Enter text or select an option",
                #     style={"width":"50%", "justify-content":"right"},
                # ),
                html.Button("Submit", id="rss-submit", n_clicks=0),
            ],
        ),
        # html.Div(id="rss-output", children="nothing yet"),
        # html.Div(' '),
        html.Div(
            id='rss-output', 
            style={
                'overflowY': 'scroll', 
                # 'height': '500px', 
                # 'border': '1px solid black'
            }
        )
    ]
)


# Define callbacks
# @app.callback(
#     Output("modal-fs", "is_open"),
#     Output("saved-api-key", "value"),
#     Input("api-key-submit", "n_clicks"),
#     State("user-api-key", "value"),
# )
# def log_api_key(n_clicks, key_input):
#     if n_clicks > 0:
#         # NOTE: need to also test the API key before closing modal
#         return False, key_input
#     else:
#         return True, None

@app.callback(
    Output("rss-output", "children"),
    Input("rss-submit", "n_clicks"),
    State("rss-input", "value"),
)
def update_output(n_clicks, url):
    if n_clicks > 0:
        try:
            feed = get_rss_feed(url)['entries']
            
            # print()
            # print(json.dumps(feed, indent=4))
            
            children = []
            for f in feed:
                card = dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(f['title']),
                            html.P(f['description']),
                            dbc.CardLink("Open Link", href=f['link']),
                        ]
                    )
                )
                children.append(card)
            return children
        except Exception as e:
            print(traceback())
            print()
            print(e)
            return ["Invalid link, please doublecheck."]


if __name__ == "__main__":
    app.run_server(debug=True)

    # for prod:
    # application.debug = True
    # application.run(port=80)
