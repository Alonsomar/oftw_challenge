import dash_bootstrap_components as dbc
from dash import html

def home_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Welcome to the OFTW Dashboard"),
                html.P("Please select a section in the sidebar to begin.")
            ], width=12)
        ], style={"marginTop": "50px"})
    ], fluid=True)
