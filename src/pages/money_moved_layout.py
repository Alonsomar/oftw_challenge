# src/pages/money_moved_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def money_moved_layout():
    return dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Money Moved Analysis", className="display-4 text-center mb-3 fade-in"),
                    html.P("Track and analyze money movement across different channels and platforms", className="lead text-center mb-5 fade-in")
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # Main Money Moved Graph
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-money-bill-wave fa-2x mb-3"),
                        html.H3("Money Moved", className="mb-4"),
                        dcc.Graph(id="money-moved-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # Counterfactual Money Moved
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x mb-3"),
                        html.H3("Counterfactual Money Moved", className="mb-4"),
                        dcc.Graph(id="counterfactual-money-moved-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # Split View Graphs
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-credit-card fa-2x mb-3"),
                        html.H3("Money Moved by Payment Platform", className="mb-4"),
                        dcc.Graph(id="money-moved-platform-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-hand-holding-heart fa-2x mb-3"),
                        html.H3("Money Moved by Donation Type", className="mb-4"),
                        dcc.Graph(id="money-moved-donation-type-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=6)
        ], className="mb-5 g-4"),

        # Treemap Graph
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-sitemap fa-2x mb-3"),
                        html.H3("Money Moved by Source (Treemap)", className="mb-4"),
                        dcc.Graph(id="money-moved-source-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ]),

    ], fluid=True, className="py-4")
