import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.section import section

dash.register_page(__name__, path="/", name="Home")

layout = dbc.Container([
    # SECTION 1
    section("Clusters a partir de la densidad poblacional y la adopción digital", [
        dbc.Row([
            dbc.Col(html.Img(id="img-map", className="map-img"), md=6),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-prom-pobl"))), md=3),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-cobertura-cluster"))), md=3),
        ], className="gy-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-adop-por-cluster"))), md=6)
        ], className="gy-3 mt-1")
    ]),

    # SECTION 2
    section("Clusters a partir de las variables sociodemográficas y la adopción digital", [
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-scatter-clusters"))), md=6),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-genero"))), md=6),
        ], className="gy-3"),
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-estrato-prom"))), md=6),
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-escolaridad-prom"))), md=6),
        ], className="gy-3")
    ]),

    # SECTION 3
    section("Patrones de adopción digital", [
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-patrones"))), md=12)
        ])
    ]),

    # SECTION 4
    section("Top 5 de municipios con mayores necesidades de adopción digital", [
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody(dcc.Loading(dcc.Graph(id="tbl-top5")))), md=12)
        ])
    ])
], fluid=True, className="main")