# sidebar.py

import dash_bootstrap_components as dbc
from dash import html

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "60px",  # Ajustar si tienes un navbar arriba
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "1rem",
    "transition": "all 0.2s",
    "overflow": "auto",
    "boxShadow": "2px 0 10px rgba(0,0,0,0.1)",
    "zIndex": 900,
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink("Money Moved", href="/money_moved", active="exact"),
                dbc.NavLink("OKRs / Objectics", href="/objectics", active="exact"),
                dbc.NavLink("Pledge Performance", href="/pledge_perf", active="exact"),
                # ... etc
            ],
            vertical=True,
            pills=True,
            className="sidebar-nav"
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE
)
