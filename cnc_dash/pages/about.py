import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About & notes")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("About this prototype"),
            html.P("This Dash app is a styled template aligned to the project mockup: "
                   "overview KPIs, territorial view with ranking, population segments, what-if scenarios, and a data explorer."),
            html.Ul([
                html.Li("Replace synthetic sample data with your ETL output."),
                html.Li("Connect a GeoJSON to render the choropleth on the Territorial page."),
                html.Li("Plug your clustering and policy models into callbacks in src/callbacks.py."),
            ]),
        ])), md=12)
    ], className="gy-3 mt-2")
], fluid=True)