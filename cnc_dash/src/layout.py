from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from src.components.kpi_chip import kpi_chip
from src.components.section import section


def _header():
    # top title + compact filter row + KPI chips, sticks to top
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Div("Análisis de la adopción digital en Colombia", className="title"), md=8),
                dbc.Col(html.Div([
                    dbc.Button("About & notes", href=dash.get_relative_path('/about'), color="secondary", outline=True)
                ], className="text-end"), md=4)
            ], className="g-2"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id="f-depto", placeholder="Departamento", multi=True), md=3),
                dbc.Col(dcc.Dropdown(id="f-area", placeholder="Área geográfica", multi=True), md=3),
                dbc.Col(kpi_chip("kpi-cobertura", "Cobertura", "95%"), md=3),
                dbc.Col(kpi_chip("kpi-adop", "Adopción digital", "45%"), md=3),
            ], className="g-2 mt-1 filters")
        ], fluid=True)
    ], className="header py-2")


def _scroll_body():
    # Sections stacked vertically to mimic your mockup
    return dbc.Container([
        # SECTION 1: Clusters densidad + adopción (map + three small charts)
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

        # SECTION 2: Clusters con variables sociodemográficas
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

        # SECTION 3: Patrones de adopción digital (stacked bars)
        section("Patrones de adopción digital", [
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Graph(id="fig-patrones"))), md=12)
            ])
        ]),

        # SECTION 4: Top 5 municipios con mayores necesidades
        section("Top 5 de municipios con mayores necesidades de adopción digital", [
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody(dcc.Loading(dcc.Graph(id="tbl-top5")))), md=12)
            ])
        ])
    ], fluid=True, className="main")


def make_shell():
    return html.Div([
        _header(),
        _scroll_body(),
        dcc.Store(id="store-data"),
        dcc.Store(id="store-filters"),
        dcc.Store(id="store-metadata"),
    ])