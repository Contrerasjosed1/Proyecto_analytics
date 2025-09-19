import dash
from dash import html
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="CNC – Digital Adoption Panel",
)
server = app.server

from src.layout import make_shell
from src import callbacks as _register_callbacks  # noqa: F401  # registers callbacks

app.layout = make_shell()

if __name__ == "__main__":
    run = getattr(app, "run", app.run)
    run(debug=True)