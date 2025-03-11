"""
Define la estructura visual de la aplicación Dash.
Este script solo maneja la UI, la carga de datos y los callbacks se manejan por separado.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.data_ingestion.data_loader import load_clean_data
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved

# Layout con dcc.Store() para evitar recargas innecesarias
def create_layout():
    return dbc.Container([
        html.H1("OFTW Money Moved Dashboard", style={"textAlign": "center"}),

        # Almacenar datos en el cliente para evitar recargas
        dcc.Store(id="stored-data", storage_type="memory"),

        # Filtros
        dbc.Row([
            dbc.Col([
                html.Label("Select Year"),
                dcc.Dropdown(id="year-filter", multi=True, placeholder="Select year(s)")
            ], width=3),

            dbc.Col([
                html.Label("Select Portfolio"),
                dcc.Dropdown(id="portfolio-filter", multi=True, placeholder="Select portfolio(s)")
            ], width=3),
        ], style={"marginBottom": "20px"}),

        # Gráficos
        dbc.Row([
            dbc.Col([
                html.H3("Money Moved"),
                dcc.Graph(id="money-moved-graph", figure=go.Figure())  # Callback actualizará esto
            ], width=12)
        ], style={"marginBottom": "40px"}),

        dbc.Row([
            dbc.Col([
                html.H3("Counterfactual Money Moved"),
                dcc.Graph(id="counterfactual-money-moved-graph", figure=go.Figure())  # Callback actualizará esto
            ], width=12)
        ])
    ], fluid=True)
