import dash_bootstrap_components as dbc
from dash import html, dcc

def home_layout():
    return dbc.Container([
        # HERO SECTION
        dbc.Row(
            dbc.Col(
                html.Div([
                    # Hero Content
                    html.H1(
                        "Welcome to the OFTW Dashboard",
                        className="display-3 text-center mb-4 hero-title fade-in"
                    ),
                    html.P(
                        "Discover insights on organizational pledges, donations, and overall performance metrics — all in one place.",
                        className="lead text-center fade-in",
                        style={"maxWidth": "700px", "margin": "0 auto"}
                    ),
                    dbc.Button(
                        "Get Started",
                        # Removed color="primary" to rely fully on custom styling
                        className="mt-4 fade-in",
                        style={
                            "background": "linear-gradient(45deg, #2675f8, #dc0073)",
                            "borderRadius": "30px",
                            "color": "#fff",
                            "fontWeight": "600",
                            "fontSize": "1.2rem",
                            "padding": "12px 30px",
                            "border": "none",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                            "cursor": "pointer"
                        },
                        href="/money_moved"
                    )
                ],
                className="hero-home p-5 text-light"
                ),
                width=12
            ),
            className="mb-5"
        ),

        # FEATURE CARDS SECTION
        dbc.Row([
            # Card 1
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-3x mb-3", style={"color": "#2675f8"}),
                        html.H4("Track the Organization's Money Moved", className="mb-3"),
                        html.P(
                            "Monitor total donation amounts, detect trends, and understand how funds "
                            "are being allocated across the organization."
                        ),
                    ], className="feature-card-content"),
                ], className="info-card fade-in")
            ], md=4, sm=12),

            # Card 2
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-bullseye fa-3x mb-3", style={"color": "#dc0073"}),
                        html.H4("Align with Our OKRs", className="mb-3"),
                        html.P(
                            "Stay on top of core metrics like ARR, total active donors, and pledge "
                            "attrition to keep your organizational objectives on track."
                        ),
                    ], className="feature-card-content"),
                ], className="info-card fade-in")
            ], md=4, sm=12),

            # Card 3
            dbc.Col([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-handshake fa-3x mb-3", style={"color": "#fb6a37"}),
                        html.H4("Optimize Pledge Performance", className="mb-3"),
                        html.P(
                            "Explore future pledges, monthly attrition, and donor engagement details "
                            "to refine strategies and maximize the organization's impact."
                        ),
                    ], className="feature-card-content"),
                ], className="info-card fade-in")
            ], md=4, sm=12),
        ], className="g-4 mb-5"),

        # CTA / EXPLANATION SECTION
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2("Ready to Explore More?", className="mb-3 text-center slide-in"),
                    html.P(
                        "Use the sidebar on the left to navigate between different sections — "
                        "from comprehensive donation breakdowns to in-depth pledge performance metrics.",
                        className="text-center",
                        style={"maxWidth": "800px", "margin": "0 auto"}
                    ),
                    dbc.Button(
                        "View Methodological Notes",
                        outline=True,
                        color="secondary",
                        className="mx-auto d-block mt-4 slide-in",
                        href="/notes",
                        style={
                            "fontWeight": "600",
                            "fontSize": "1rem",
                            "borderRadius": "30px"
                        }
                    ),
                ], className="p-4")
            ], width=12)
        ], className="mb-5"),
    ],
    fluid=True,
    className="home-container py-4"
)
