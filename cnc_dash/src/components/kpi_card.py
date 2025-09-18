from dash import html
import dash_bootstrap_components as dbc

def kpi_card(card_id: str, title: str, value: str = "—", helptext: str = ""):
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.H4(title, className="kpi"),
                html.H2(value, id=card_id, className="kpi")
            ]),
            html.Small(helptext, className="text-muted") if helptext else None
        ]), className="h-100")