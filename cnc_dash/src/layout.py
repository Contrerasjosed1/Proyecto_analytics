from dash import html, dcc
import dash
import dash_bootstrap_components as dbc


def _sidebar():
    # Build navigation from registered pages
    nav_items = []
    for page in dash.page_registry.values():
        nav_items.append(
            dbc.NavLink(page["name"], href=page["path"], active="exact", className="mb-1")
        )

    return html.Div([
        html.Div([
            html.Div("CNC – Digital Adoption", className="app-title"),
            html.Div("Prototipo tablero analítico", className="subtitle")
        ], className="mb-3"),
        dbc.Nav(nav_items, vertical=True, pills=True),
        html.Hr(),
        html.Div([
            html.Small("Filters apply across pages"),
            html.Div(className="mt-2"),
            dbc.Label("Year"),
            dcc.Dropdown(id="f-year", multi=False, placeholder="All", clearable=True),
            dbc.Label("Department", className="mt-2"),
            dcc.Dropdown(id="f-depto", multi=True, placeholder="All"),
            dbc.Label("Municipality", className="mt-2"),
            dcc.Dropdown(id="f-muni", multi=True, placeholder="All"),
            dbc.Label("Strata", className="mt-2"),
            dcc.Checklist(id="f-estrato", inline=True, options=[1,2,3,4,5,6], value=[1,2,3,4,5,6]),
            dbc.Label("Age range", className="mt-2"),
            dcc.RangeSlider(id="f-edad", min=12, max=80, step=1, value=[16,70], allowCross=False),
            dbc.Checklist(id="f-internet", options=[{"label":"With Internet only","value":"with"}], value=[]),
        ], className="filters")
    ], className="sidebar")


def _topbar():
    return html.Div([
        html.Div("Digital Adoption Panel – CNC", className="h5 m-0"),
        html.Div([
            dbc.Button("Export view", id="btn-export", color="primary", outline=True, className="me-2"),
            dbc.Button("Refresh data", id="btn-refresh", color="secondary", outline=True)
        ])
    ], className="topbar")


def make_shell(shared_stores):
    return dbc.Container([
        dbc.Row([
            dbc.Col(_sidebar(), width=3),
            dbc.Col([
                _topbar(),
                dash.page_container,
                shared_stores
            ], width=9)
        ], className="g-0")
    ], fluid=True)
