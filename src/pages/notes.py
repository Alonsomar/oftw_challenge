import dash_bootstrap_components as dbc
from dash import html

code_style = {"fontSize": "100%"}

def notes_layout():
    return dbc.Container([
        # Page Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Methodological Notes and Findings", className="display-4 text-center mb-3 fade-in"),
                    html.P(
                        "This section covers the currency conversion process, the main data transformations, "
                        "key performance metrics, and the overall structure of the application's codebase.",
                        className="lead text-center mb-5 fade-in"
                    )
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # Content Sections
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("1. Currency Conversion"),
                    html.P([
                        "• All monetary amounts are converted to USD using the ",
                        html.Code("currency_converter", style=code_style),
                        " library and historical rates stored in ",
                        html.Code("eurofxref-hist.csv", style=code_style),
                        ". For future pledges, the most recent available rate is applied.",
                        html.Br(),
                        "• Specific portfolios, such as ",
                        html.Code("One for the World Discretionary Fund", style=code_style),
                        " and ",
                        html.Code("One for the World Operating Costs", style=code_style),
                        ", are excluded from Money Moved calculations to focus on core charitable donations."
                    ]),

                    html.H3("2. Date and Period Handling"),
                    html.P([
                        "• Users can filter data by calendar years (",
                        html.Code("Jan 1 – Dec 31", style=code_style),
                        ") or fiscal years (",
                        html.Code("Jul 1 – Jun 30", style=code_style),
                        ").",
                        html.Br(),
                        "• Monthly aggregations (",
                        html.Code("YYYY-MM", style=code_style),
                        ") are used throughout most visualizations."
                    ]),

                    html.H3("3. Money Moved Calculation"),
                    html.P([
                        "• The system sums donation amounts (in USD) monthly and cumulatively, excluding portfolios not directly ",
                        "allocated to recommended charities.",
                        html.Br(),
                        "• Counterfactual Money Moved multiplies each donation by its respective ",
                        html.Code("counterfactuality", style=code_style),
                        " factor (0–1), reflecting the proportion of the donation truly attributable to OFTW’s outreach."
                    ]),

                    html.H3("4. OKRs (Objectives and Key Results)"),
                    html.P([
                        "• The total number of ",
                        html.Code("Active Donors", style=code_style),
                        " includes both ",
                        html.Code("One-time donor", style=code_style),
                        " and ",
                        html.Code("Active donor", style=code_style),
                        " statuses.",
                        html.Br(),
                        "• Pledge Attrition Rate is the fraction of pledges ending up in ",
                        html.Code("Payment failure", style=code_style),
                        " or ",
                        html.Code("Churned donor", style=code_style),
                        " among all recurrent pledges.",
                        html.Br(),
                        "• Chapter ARR aggregates annualized amounts by ",
                        html.Code("chapter_type", style=code_style),
                        " for 'Active donor' and 'Pledged donor' statuses."
                    ]),

                    html.H3("5. Pledge Performance Metrics"),
                    html.P([
                        "• Future pledges are those labeled ",
                        html.Code("Pledged donor", style=code_style),
                        "—not yet active.",
                        html.Br(),
                        "• ALL ARR encompasses both pledged and active donors. ",
                        html.Code("Future ARR", style=code_style),
                        " applies only to 'Pledged donor', while ",
                        html.Code("Active ARR", style=code_style),
                        " applies to 'Active donor'.",
                        html.Br(),
                        "• Monthly attrition indicates how many pledges were lost during a given month compared with those active in the same period."
                    ]),

                    html.H3("6. Consistency Checks"),
                    html.P([
                        "• By definition, the total number of ",
                        html.Code("Active Donors", style=code_style),
                        " should be greater than or equal to the total number of ",
                        html.Code("Active Pledges", style=code_style),
                        ".",
                        html.Br(),
                        "• Any discrepancies trigger log warnings to facilitate data validation."
                    ]),

                    html.H3("7. Application Structure"),
                    html.P([
                        "• The app is built with ",
                        html.Code("Dash", style=code_style),
                        " and ",
                        html.Code("Dash Bootstrap Components", style=code_style),
                        ", with Plotly powering data visualization.",
                        html.Br(),
                        "• Data ingestion and transformations live in ",
                        html.Code("src/data_ingestion", style=code_style),
                        ", while metric definitions reside in ",
                        html.Code("src/metrics_calculations", style=code_style),
                        ".",
                        html.Br(),
                        "• Callbacks (in ",
                        html.Code("src/callbacks", style=code_style),
                        ") handle interactivity, and caching (via ",
                        html.Code("flask_caching", style=code_style),
                        ") aids performance.",
                        html.Br(),
                        "• The color palette and layout follow OFTW’s official branding, specified in ",
                        html.Code("assets/styles.css", style=code_style),
                        " and a custom ",
                        html.Code("oftw_template", style=code_style),
                        " (",
                        html.Code("theme.py", style=code_style),
                        ")."
                    ]),

                    html.H3("8. Data Usage"),
                    html.P([
                        "• The dashboard aims to quantify donation impact and monitor pledge commitments over time.",
                        html.Br(),
                        "• All metrics can be influenced by data completeness, correct attribution factors, and currency updates.",
                        html.Br(),
                        "• Users can apply portfolio and year filters, but should confirm data accuracy when interpreting ",
                        html.Code("Money Moved", style=code_style),
                        ", ",
                        html.Code("ARR", style=code_style),
                        ", or ",
                        html.Code("attrition", style=code_style),
                        " rates."
                    ]),

                ], className="card info-card fade-in")
            ], width=12)
        ])
    ], fluid=True, className="py-4")
