import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__, path="/segments", name="Population segments")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-seg-scatter"))), md=7),
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-seg-bars"))), md=5),
    ], className="gy-3 mt-2"),
    html.Div(className="mb-3")
], fluid=True)