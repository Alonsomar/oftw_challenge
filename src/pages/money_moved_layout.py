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
                        html.P(
                            "Monthly donation totals reveal how giving levels evolve over time, helping to gauge momentum, spot trends, and measure progress toward OFTW’s mission.",
                            className="graph-explanation"
                        ),
                        dcc.Graph(id="money-moved-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ], className="mb-5"),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-area fa-2x mb-3"),
                        html.H3("Accumulated Money Moved", className="mb-4"),
                        html.P(
                            "Cumulative totals, calculated year by year (fiscal or calendar), offer a clear snapshot of how quickly we approach annual goals, highlighting donation surges or slowdowns.",
                            className="graph-explanation"
                        ),
                        dcc.Graph(id="accumulated-money-moved-graph", figure=go.Figure())
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
                        html.P(
                            "Highlights the portion of donations uniquely driven by OFTW’s outreach, based on a 0–1 counterfactuality factor. This illustrates the net-new philanthropic impact attributable to our efforts.",
                            className="graph-explanation"
                        ),
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
                        html.P(
                            "Shows how much each payment channel contributes, helping identify top-performing platforms and potential areas for streamlining donor experiences.",
                            className="graph-explanation"
                        ),
                        dcc.Graph(id="money-moved-platform-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=6),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-hand-holding-heart fa-2x mb-3"),
                        html.H3("Money Moved by Donation Type", className="mb-4"),
                        html.P(
                            "Compares one-time vs. recurring contributions, revealing the balance between short-term influxes of support and the long-term stability provided by sustained donors.",
                            className="graph-explanation"
                        ),
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
                        html.P(
                            "Displays how different donor chapters and chapter types contribute, allowing deeper insight into which segments generate the greatest share of overall funding.",
                            className="graph-explanation"
                        ),
                        dcc.Graph(id="money-moved-source-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ]),

    ], fluid=True, className="py-4")
