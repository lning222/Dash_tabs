import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash import html
from dash import dcc, dash_table
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import twitter  # pip install python-twitter
from app import app, api
from collections import OrderedDict

# Connect to the layout and callbacks of each tab
from mentions import mentions_layout
from trends import trends_layout
from other import other_layout

# data used:
data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)
df = pd.DataFrame(data)

data_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        fixed_rows={'headers': True},
        # style_cell refers to the whole table
        style_cell={'textAlign': 'left', 'padding': '1px', 'minWidth': 95, 'maxWidth': 95, 'width': 95},
        style_header={
                'backgroundColor': 'rgb(230, 230, 230)', #darker grey
                'fontWeight': 'bold'
            },
        # style_data.c refers only to data rows
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)' # light grey
            }
        ],
        # no vertical grid
        style_as_list_view=True,
    )

# ********** our app's Tabs ****************

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="counterparty info", tab_id="tab-counterparty-info",
                        labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="structure legs", tab_id="tab-structure-legs",
                        labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="strike pnl", tab_id="tab-strike-pnl", labelClassName="text-success font-weight-bold",
                        activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-counterparty-info",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    # dash width max = 12, 'width=12' means full length
    dbc.Row(dbc.Col(html.H1("Wholesale and DCP analyser",
                            style={"textAlign": "center"}),
                    width=12)
            ),
    # add a horizontal line
    html.Hr(),
    # structure id input
    dbc.Row(dbc.Col(children=[
        html.Label("Search contract ID:",
                   style={'textAlign': 'left', 'marginRight': '5px'},
                   ),
        dcc.Input(
            id="input-contract-id",
            type="text",
            placeholder="contract id here",
            value="",
        ),
    ],
    ), className="mb-3"
    ),

    # table of the legs
    dbc.Row(dbc.Col(children=data_table
    ), className="b-3",
    ),

    # tabs
    dbc.Row(dbc.Col(children=app_tabs, width=12)),

    # main content to display
    html.Div(id='content', children=[])

])

# switch the tab
@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-counterparty-info":
        return mentions_layout
    elif tab_chosen == "tab-structure-legs":
        return trends_layout
    elif tab_chosen == "tab-strike-pnl":
        return other_layout
    return html.P("This shouldn't be displayed for now...")


if __name__ == '__main__':
    app.run_server(debug=True)
