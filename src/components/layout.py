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
        dcc.Store(id="store-filtered-data", storage_type="memory"),
        dcc.Location(id="url", refresh=False),

        # HEADER SUPERIOR (Fixed)
        create_header(),

        # SIDEBAR (Fixed)
        sidebar,

        # Contenedor principal
        html.Div([
            # FILTROS GLOBALES
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Label("Select Year", className="filter-label"),
                        dcc.Dropdown(
                            id="year-filter",
                            multi=True,
                            placeholder="Select year(s)",
                            className="dash-dropdown"
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label("Select Portfolio", className="filter-label"),
                        dcc.Dropdown(
                            id="portfolio-filter",
                            multi=True,
                            placeholder="Select portfolio(s)",
                            className="dash-dropdown"
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label("Year Mode", className="filter-label"),
                        dcc.Dropdown(
                            id="year-mode",
                            options=[
                                {"label": "Fiscal Year (Jul-Jun)", "value": "fiscal"},
                                {"label": "Calendar Year (Jan-Dec)", "value": "calendar"}
                            ],
                            value="fiscal",
                            clearable=False,
                            className="dash-dropdown"
                        )
                    ], width=4),
                ], className="g-3")
            ], className="filter-section fade-in"),

            # Contenido de la página
            html.Div(
                id="page-content",
                className="fade-in"
            ),
        ], className="main-content"),
    ])
