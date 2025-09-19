import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About & notes")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("About this prototype"),
            html.P("Scroll-first Dash layout aligned to the provided mockup: sticky header with filters and KPI chips; sections for choropleth + cluster summaries, socio-demographic clusters, behavioral patterns, and a needs ranking. Replace the sample data and map join with your ETL outputs."),
            html.Ul([
                html.Li("Map: built with GeoPandas/Matplotlib to match your hatch + OrRd style. Adjust shapefile paths in src/config.py."),
                html.Li("Charts: Plotly figures; plug real models in src/callbacks.py."),
            ])
        ])), md=12)
    ], className="gy-3 mt-2")
], fluid=True)