import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.kpi_card import kpi_card

dash.register_page(__name__, path="/", name="Overview")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(kpi_card("kpi-pop", "Observations", "—"), md=3),
        dbc.Col(kpi_card("kpi-idx", "Adoption index (avg)", "—"), md=3),
        dbc.Col(kpi_card("kpi-coverage", ">0.67 coverage", "—"), md=3),
        dbc.Col(kpi_card("kpi-inet", "Internet access share", "—"), md=3),
    ], className="gy-3 mt-2"),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-idx-depto"))), md=7),
        dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-estrato"))), md=5)
    ], className="gy-3 mt-1"),
    html.Div(className="mb-3")
], fluid=True)