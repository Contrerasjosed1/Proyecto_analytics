import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table


dash.register_page(__name__, path="/data", name="Data explorer")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Dataset snapshot"),
            dash_table.DataTable(
                id="tbl-data",
                page_size=15,
                sort_action="native",
                filter_action="native",
                style_table={"height":"600px","overflowY":"auto"},
                style_cell={"fontSize":"12px","padding":"6px"},
                columns=[{"name": c, "id": c} for c in [
                    "year","departamento","municipio","estrato","edad",
                    "acceso_internet","dens_int","idx_adopcion","cluster"
                ]],
            ),
        ])), md=12)
    ], className="gy-3 mt-2")
], fluid=True)