import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table


dash.register_page(__name__, path="/territorial", name="Territorial map & ranking")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Territorial heatmap"),
            html.Div("Connect a GeoJSON to render a choropleth. Placeholder below.", className="placeholder"),
            dcc.Graph(figure={})
        ])), md=7),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Municipalities with lowest adoption (Top 50)"),
            dash_table.DataTable(
                id="table-ranking",
                page_size=10,
                sort_action="native",
                filter_action="native",
                style_table={"height":"520px","overflowY":"auto"},
                style_cell={"fontSize":"12px","padding":"6px"},
            )
        ])), md=5)
    ], className="gy-3 mt-2")
], fluid=True)