import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.section import section

dash.register_page(__name__, path="/", name="Home")

layout = dbc.Container([
    # SECTION 1
    section("Clusters a partir de la densidad poblacional y la adopción digital", [
    # Fila principal: Mapa (izq) y dos charts apiladas (der)
    dbc.Row([
        # Columna izquierda: Mapa
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    html.Img(id="img-map", className="map-img",
                             style={"display": "block", "width": "100%", "height": "100%", "objectFit": "contain"})
                ),
            ),
            md=6, className="mb-3"
        ),

        # Columna derecha: dos gráficas apiladas
        dbc.Col([
            dbc.Row(
                dbc.Col(
                    dbc.Card(dbc.CardBody(dcc.Graph(id="fig-prom-pobl"))),
                    width=12
                ),
                className="mb-3"
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(dbc.CardBody(dcc.Graph(id="fig-cobertura-cluster"))),
                    width=12
                )
            ),
        ], md=6, className="mb-3"),
    ], className="gy-3"),

    # Fila inferior: gráfica a lo ancho (armoniza el flujo visual)
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody(dcc.Graph(id="fig-adop-por-cluster"))),
            md=12
        )
    ], className="gy-3 mt-1"),
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