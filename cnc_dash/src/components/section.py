from dash import html

def section(title: str, children):
    return html.Div([
        html.H5(title),
        *([children] if not isinstance(children, (list, tuple)) else children)
    ], className="section")