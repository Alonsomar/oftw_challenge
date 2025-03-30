# src/pages/pledge_perf_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def pledge_perf_layout():
    return dbc.Container([
        # Header Section with Gradient Background
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Pledge Performance", className="display-4 text-center mb-3 fade-in"),
                    html.P("Track and analyze your pledge metrics in real-time", className="lead text-center mb-5 fade-in")
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # Performance Metrics Cards with Enhanced Design - First Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-hand-holding-usd fa-2x mb-3 metric-icon"),
                        html.H3("Total Pledges", className="metric-title"),
                        html.H2(id="total-pledges", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-calendar-check fa-2x mb-3 metric-icon"),
                        html.H3("Future Pledges", className="metric-title"),
                        html.H2(id="future-pledges", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x mb-3 metric-icon"),
                        html.H3("ALL ARR", className="metric-title"),
                        html.H2(id="all-arr", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
        ], className="mb-4 g-4"),

        # Performance Metrics Cards - Second Row
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-rocket fa-2x mb-3 metric-icon"),
                        html.H3("Future ARR", className="metric-title"),
                        html.H2(id="future-arr", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-bolt fa-2x mb-3 metric-icon"),
                        html.H3("Active ARR", className="metric-title"),
                        html.H2(id="active-arr", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-pie fa-2x mb-3 metric-icon"),
                        html.H3("Monthly Attrition Rate", className="metric-title"),
                        html.H2(id="monthly-attrition-rate", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
        ], className="mb-5 g-4"),

        # Channel Breakdown Graph with Enhanced Container
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-bar fa-2x mb-3"),
                        html.H3("Breakdown of Pledges by Channel", className="mb-4"),
                        dcc.Graph(
                            id="breakdown-channel-graph",
                            figure=go.Figure(),
                            className="graph-container fade-in"
                        )
                    ], className="graph-section")
                ], className="card graph-card")
            ], width=12)
        ]),

    ], fluid=True, className="py-4")
