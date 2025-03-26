# src/pages/money_moved_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def money_moved_layout():
    return dbc.Container([
        # Sección 1: Money Moved
        dbc.Row([
            dbc.Col([
                html.H3("Money Moved"),
                dcc.Graph(id="money-moved-graph", figure=go.Figure())
            ], width=12)
        ], style={"marginBottom": "40px"}),

        dbc.Row([
            dbc.Col([
                html.H3("Counterfactual Money Moved"),
                dcc.Graph(id="counterfactual-money-moved-graph", figure=go.Figure())
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                html.H3("Money Moved by Payment Platform"),
                dcc.Graph(id="money-moved-platform-graph", figure=go.Figure())
            ], width=6),
            dbc.Col([
                html.H3("Money Moved by Donation Type"),
                dcc.Graph(id="money-moved-donation-type-graph", figure=go.Figure())
            ], width=6),
        ], style={"marginBottom": "40px"}),

        dbc.Row([
            dbc.Col([
                html.H3("Money Moved by Source (Treemap)"),
                dcc.Graph(id="money-moved-source-graph", figure=go.Figure())
            ], width=12),
        ], style={"marginBottom": "40px"}),

    ], fluid=True)
