# src/pages/pledge_perf_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def pledge_perf_layout():
    return dbc.Container([

        # Performance Metrics
        dbc.Row([
            dbc.Col([
                html.H3("Total Pledges"),
                html.H2(id="total-pledges", children="Loading..."),
            ], width=2),
            dbc.Col([
                html.H3("Future Pledges"),
                html.H2(id="future-pledges", children="Loading..."),
            ], width=2),
            dbc.Col([
                html.H3("ALL ARR"),
                html.H2(id="all-arr", children="Loading..."),
            ], width=2),
            dbc.Col([
                html.H3("Future ARR"),
                html.H2(id="future-arr", children="Loading..."),
            ], width=2),
            dbc.Col([
                html.H3("Active ARR"),
                html.H2(id="active-arr", children="Loading..."),
            ], width=2),
            dbc.Col([
                html.H3("Monthly Attrition Rate"),
                html.H2(id="monthly-attrition-rate", children="Loading..."),
            ], width=2),
        ], style={"marginBottom": "40px"}),

        dbc.Row([
            dbc.Col([
                html.H3("Breakdown of Pledges by Channel"),
                dcc.Graph(id="breakdown-channel-graph", figure=go.Figure())
            ], width=12),
        ]),

    ], fluid=True)
