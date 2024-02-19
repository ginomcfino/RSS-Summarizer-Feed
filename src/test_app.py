from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict
# Import the names of callback functions
from .app import *

'''
Test Dash UI
'''

def test_callback_0():
    output = update_output(1, 0) # call the callback function update_output
    assert type(output) != Exception, 'uh oh'


# '''
# end-end pytest to see whether the dashboard is up or not

# req: selenium, chromedriver, dash[testing]
# '''
# def test_dash(dash_duo):
#     app = import_app("app")
#     dash_duo.start_server(app)
#     assert dash_duo.get_logs() == [], "uhh ohh"