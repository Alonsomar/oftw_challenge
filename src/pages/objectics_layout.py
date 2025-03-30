# src/pages/objectics_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def objectics_layout():
    return dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Objectives & Key Results", className="display-4 text-center mb-3 fade-in"),
                    html.P("Track your key performance indicators and objectives", className="lead text-center mb-5 fade-in")
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # OKRs Metrics
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-users fa-2x mb-3 metric-icon"),
                        html.H3("Total Active Donors", className="metric-title"),
                        html.H2(id="total-active-donors", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-handshake fa-2x mb-3 metric-icon"),
                        html.H3("Total Active Pledges", className="metric-title"),
                        html.H2(id="total-active-pledges", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-pie fa-2x mb-3 metric-icon"),
                        html.H3("Pledge Attrition Rate", className="metric-title"),
                        html.H2(id="pledge-attrition-rate", children="Loading...", className="metric-value"),
                    ], className="metric-content")
                ], className="metric-card fade-in")
            ], width=4),
        ], className="mb-5 g-4"),

        # Chapter ARR Graph
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x mb-3"),
                        html.H3("Chapter ARR", className="mb-4"),
                        dcc.Graph(id="chapter-arr-graph", figure=go.Figure())
                    ], className="graph-section")
                ], className="card graph-card fade-in")
            ], width=12)
        ]),

    ], fluid=True, className="py-4")
