from dash import html, dcc
import dash
import dash_bootstrap_components as dbc
from src.components.kpi_chip import kpi_chip
# from src.components.section import section   # ya no se usa aquí, va en pages/home.py

def _header():
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Div("Análisis de la adopción digital en Colombia", className="title"), md=8),
                dbc.Col(html.Div([
                    dbc.Button("About & notes", href=dash.get_relative_path('/about'),
                               color="secondary", outline=True)
                ], className="text-end"), md=4)
            ], className="g-2"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id="f-region", placeholder="Departamento", multi=False), md=3),
                dbc.Col(dcc.Dropdown(id="f-area", placeholder="Total", multi=True), md=3),
                dbc.Col(kpi_chip("kpi-cobertura", "Cobertura", "95%"), md=3),
                dbc.Col(kpi_chip("kpi-adop", "Adopción digital", "45%"), md=3),
            ], className="g-2 mt-1 filters")
        ], fluid=True)
    ], className="header py-2")

def make_shell():
    return html.Div([
        _header(),
        dash.page_container,          # ← aquí se montan / (home.py) y /about
        dcc.Store(id="store-data"),
        dcc.Store(id="store-data-filtrada"),
        dcc.Store(id="store-filters"),
        dcc.Store(id="store-metadata"),
    ])