from dash import html

def kpi_chip(id_value: str, label: str, init_value: str = "—"):
    return html.Div([
        html.Span(label, className="label"),
        html.Span(init_value, id=id_value, className="value")
    ], className="kpi-chip")