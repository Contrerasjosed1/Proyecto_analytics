import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

# External styles (Bootstrap base) + our theme in assets/theme.css
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    title="CNC – Digital Adoption Panel",
)
server = app.server

# Shared stores (available in all pages)
shared_stores = html.Div([
    dcc.Store(id="store-data", storage_type="memory"),         # full dataset
    dcc.Store(id="store-filters", storage_type="memory"),      # current filters
    dcc.Store(id="store-metadata", storage_type="memory"),     # meta (e.g., last refresh)
])

# Global shell (sidebar + page container)
from src.layout import make_shell

app.layout = make_shell(shared_stores)

# Register app-level callbacks
from src import callbacks as _register_callbacks  # noqa: F401

if __name__ == "__main__":
    app.run(debug=True)