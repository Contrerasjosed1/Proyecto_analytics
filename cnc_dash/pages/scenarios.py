import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.components.kpi_card import kpi_card


dash.register_page(__name__, path="/scenarios", name="What-if scenarios")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Intervention levers"),
            dbc.Label("Connectivity subsidy (0–100)"),
            dcc.Slider(id="scn-subsidy", min=0, max=100, step=1, value=10, tooltip={"always_visible": True}),
            dbc.Label("Training hours per person (0–100)"),
            dcc.Slider(id="scn-training", min=0, max=100, step=1, value=5, tooltip={"always_visible": True}),
            html.Div("These controls are placeholders — plug your policy models here.", className="placeholder mt-2")
        ])), md=6),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Projected outcomes"),
            dbc.Row([
                dbc.Col(kpi_card("kpi-scn-idx", "Projected adoption index", "—"), md=6),
                dbc.Col(kpi_card("kpi-scn-coverage", ">0.67 coverage", "—"), md=6),
            ])
        ])), md=6)
    ], className="gy-3 mt-2")
], fluid=True)