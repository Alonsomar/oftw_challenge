# src/pages/objectics_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

def objectics_layout():
    return dbc.Container([

        # OKRs
        dbc.Row([
            dbc.Col([
                html.H3("Total Active Donors"),
                html.H2(id="total-active-donors", children="Loading..."),
            ], width=3),
            dbc.Col([
                html.H3("Total Active Pledges"),
                html.H2(id="total-active-pledges", children="Loading..."),
            ], width=3),
            dbc.Col([
                html.H3("Pledge Attrition Rate"),
                html.H2(id="pledge-attrition-rate", children="Loading..."),
            ], width=3),
        ], style={"marginBottom": "40px"}),

        dbc.Row([
            dbc.Col([
                html.H3("Chapter ARR"),
                dcc.Graph(id="chapter-arr-graph", figure=go.Figure())
            ], width=12),
        ]),

    ], fluid=True)
