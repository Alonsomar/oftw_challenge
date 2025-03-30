import dash_bootstrap_components as dbc
from dash import html

def notes_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Methodological Notes", className="display-4 text-center mb-3 fade-in"),
                    html.P("Check the calculus of the indices", className="lead text-center mb-5 fade-in")
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),
    ], fluid=True)


