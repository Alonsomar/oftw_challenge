"""
Define la estructura visual de la aplicación Dash.
Este script solo maneja la UI, la carga de datos y los callbacks se manejan por separado.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.components.sidebar import sidebar
from src.components.header import create_header

def create_layout():
    return html.Div([
        dcc.Store(id="stored-data", storage_type="memory"),
        dcc.Location(id="url", refresh=False),

        # HEADER SUPERIOR
        create_header(),

        # SIDEBAR
        sidebar,

        # Contenedor principal a la derecha
        html.Div([

            # FILTROS GLOBALES => "header" de la parte central
            dbc.Row([
                dbc.Col([
                    html.Label("Select Year"),
                    dcc.Dropdown(id="year-filter", multi=True, placeholder="Select year(s)")
                ], width=3),
                dbc.Col([
                    html.Label("Select Portfolio"),
                    dcc.Dropdown(id="portfolio-filter", multi=True, placeholder="Select portfolio(s)")
                ], width=3),
                dbc.Col([
                    html.Label("Year Mode"),
                    dcc.Dropdown(
                        id="year-mode",
                        options=[
                            {"label": "Fiscal Year (Jul-Jun)", "value": "fiscal"},
                            {"label": "Calendar Year (Jan-Dec)", "value": "calendar"}
                        ],
                        value="fiscal",
                        clearable=False
                    )
                ], width=3),
            ], style={"marginBottom": "20px"}),

            # AQUI: Div vacio donde inyectaremos la “pagina” segun la URL
            html.Div(id="page-content",
                     style={"padding": "2rem"}),
        ],
            style={
                "marginLeft": "16rem",  # Deja espacio para el sidebar
                "padding": "2rem"
            }
        ),
    ])
