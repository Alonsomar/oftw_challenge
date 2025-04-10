import dash_bootstrap_components as dbc
from dash import html

code_style = {"fontSize": "100%"}

def notes_layout():
    return dbc.Container([
        # Page Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Methodological Notes and App Overview", className="display-4 text-center mb-3 fade-in"),
                    html.P(
                        "This page outlines key data assumptions, transformations, metrics definitions, and "
                        "the overall architecture of the codebase, including the new Chat LLM feature.",
                        className="lead text-center mb-5 fade-in"
                    )
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # TABLE OF CONTENTS
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Table of Contents", className="mb-4"),
                    html.Ul([
                        html.Li(html.A("1. Data Ingestion & Cleaning", href="#data-ingestion")),
                        html.Li(html.A("2. Currency Conversion & Filtering", href="#currency-conversion")),
                        html.Li(html.A("3. Date and Period Handling", href="#date-handling")),
                        html.Li(html.A("4. Metrics: Money Moved", href="#money-moved")),
                        html.Li(html.A("5. Metrics: OKRs & Performance", href="#okrs-performance")),
                        html.Li(html.A("6. Consistency Checks & Logging", href="#consistency-checks")),
                        html.Li(html.A("7. Application Structure", href="#application-structure")),
                        html.Li(html.A("8. The Chat LLM Page", href="#chat-llm")),
                        html.Li(html.A("9. Additional Notes / FAQs", href="#additional-notes")),
                    ], style={"listStyleType": "none", "paddingLeft": "0"}),
                ], className="info-card p-4 fade-in")
            ], width=12)
        ], className="mb-5"),

        # 1. DATA INGESTION & CLEANING
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("1. Data Ingestion & Cleaning", id="data-ingestion"),
                    html.P([
                        "• Data files are read from JSON in the ",
                        html.Code("src/data_ingestion/data_read.py", style=code_style),
                        " module. We store them in memory as pandas DataFrames. ",
                        html.Br(),
                        "• Cleaning steps, such as date parsing and handling empty/n/a cells, occur in ",
                        html.Code("src/data_ingestion/data_transform.py", style=code_style),
                        ". We unify missing values (\"\", \"n/a\") and set them to ",
                        html.Code("Unknown", style=code_style),
                        " in certain columns. ",
                        html.Br(),
                        "• After these transformations, columns like ",
                        html.Code("pledge_status", style=code_style),
                        " are standardized so that metrics can be calculated easily across the app."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 2. CURRENCY CONVERSION & FILTERING
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("2. Currency Conversion & Filtering", id="currency-conversion"),
                    html.P([
                        "• All monetary amounts are converted to USD using the ",
                        html.Code("currency_converter", style=code_style),
                        " library and historical exchange rates (",
                        html.Code("eurofxref-hist.csv", style=code_style),
                        "). For future pledges, we apply the latest available rate. ",
                        html.Br(),
                        "• Certain portfolios (e.g. ",
                        html.Code("One for the World Discretionary Fund", style=code_style),
                        " / ",
                        html.Code("Operating Costs", style=code_style),
                        ") are excluded from Money Moved. This ensures only recommended charitable donations are counted. ",
                        html.Br(),
                        "• The filtering logic for years and portfolios is in ",
                        html.Code("src/utils/callbacks_filter.py", style=code_style),
                        ", which merges user selections into a mask for both payments and pledges."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 3. DATE AND PERIOD HANDLING
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("3. Date and Period Handling", id="date-handling"),
                    html.P([
                        "• We support both ",
                        html.Code("calendar", style=code_style),
                        " and ",
                        html.Code("fiscal", style=code_style),
                        " modes. ",
                        html.Br(),
                        "• For calendar mode (Jan 1 – Dec 31), each year is straightforward. ",
                        html.Br(),
                        "• For fiscal mode (Jul 1 – Jun 30), a pledge in July 2024 belongs to FY 2024, while June 2025 remains the end of FY 2024. ",
                        html.Br(),
                        "• Monthly aggregations (",
                        html.Code("YYYY-MM", style=code_style),
                        ") appear across the majority of metrics to display donation trends over time."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 4. MONEY MOVED
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("4. Metrics: Money Moved", id="money-moved"),
                    html.P([
                        "• We sum up valid donations converted to USD each month, ignoring excluded portfolios. This sum is displayed in both monthly and accumulated (cumulative) views. ",
                        html.Br(),
                        "• ",
                        html.Code("Counterfactuality", style=code_style),
                        " (0–1) indicates how much of that donation is truly caused by OFTW. Multiplying donation amount by this factor yields the 'Counterfactual Money Moved'. ",
                        html.Br(),
                        "• See ",
                        html.Code("src/metrics_calculations/money_metrics.py", style=code_style),
                        " and ",
                        html.Code("src/metrics_vizualizations/money_viz.py", style=code_style),
                        " for the core logic and plotting code."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 5. OKRS & PERFORMANCE
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("5. Metrics: OKRs & Performance", id="okrs-performance"),
                    html.P([
                        "• ",
                        html.Code("Active Donors", style=code_style),
                        " includes both ",
                        html.Code("Active donor", style=code_style),
                        " and ",
                        html.Code("One-time donor", style=code_style),
                        " statuses (if one-time is relevant). ",
                        html.Br(),
                        "• ",
                        html.Code("Pledge Attrition Rate", style=code_style),
                        " is how many pledges ended up in ",
                        html.Code("Payment failure", style=code_style),
                        " or ",
                        html.Code("Churned donor", style=code_style),
                        " status, relative to the total. ",
                        html.Br(),
                        "• ",
                        html.Code("ARR (Annualized Run Rate)", style=code_style),
                        " is computed from pledge frequencies: monthly pledges × 12, quarterly × 4, etc., defined in ",
                        html.Code("src/utils/financial.py", style=code_style),
                        ". ",
                        html.Br(),
                        "• We also handle ",
                        html.Code("Semi-monthly", style=code_style),
                        " pledges (counting as 24 times per year). An unknown frequency defaults to zero annualization."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 6. CONSISTENCY CHECKS & LOGGING
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("6. Consistency Checks & Logging", id="consistency-checks"),
                    html.P([
                        "• The app logs warnings if the number of active donors is less than active pledges, or if unknown frequencies appear in the pledge data. ",
                        html.Br(),
                        "• All logging is managed via the ",
                        html.Code("loguru", style=code_style),
                        " library, configured in ",
                        html.Code("log_config.py", style=code_style),
                        ". ",
                        html.Br(),
                        "• Additional data validation steps can be added if you suspect missing or malformed data."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 7. APPLICATION STRUCTURE
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("7. Application Structure", id="application-structure"),
                    html.P([
                        "• Built using ",
                        html.Code("Dash", style=code_style),
                        " + ",
                        html.Code("Dash Bootstrap Components", style=code_style),
                        " with Plotly for visualizations. ",
                        html.Br(),
                        "• Data loading, transformations, and caching reside under ",
                        html.Code("src/data_ingestion", style=code_style),
                        " and ",
                        html.Code("src/utils/cache.py", style=code_style),
                        ". ",
                        html.Br(),
                        "• Metrics are defined in ",
                        html.Code("src/metrics_calculations", style=code_style),
                        "; callbacks that wire the UI are in ",
                        html.Code("src/callbacks", style=code_style),
                        ". ",
                        html.Br(),
                        "• The color palette and shared style rules are defined in ",
                        html.Code("assets/styles.css", style=code_style),
                        " plus the custom Plotly template in ",
                        html.Code("theme.py", style=code_style),
                        "."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 8. THE CHAT LLM PAGE
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("8. The Chat LLM Page", id="chat-llm"),
                    html.P([
                        "• The newest addition is a chat interface in ",
                        html.Code("src/pages/chat_llm_layout.py", style=code_style),
                        " that lets you ask data-oriented questions. ",
                        html.Br(),
                        "• We rely on an OpenAI LLM (see ",
                        html.Code("OPENAI_API_KEY", style=code_style),
                        " in your environment) to answer queries about filtered data. The logic is in ",
                        html.Code("chat_llm_callbacks.py", style=code_style),
                        ". ",
                        html.Br(),
                        "• If the user question is too long or the data is insufficient, the callback returns an appropriate disclaimer."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

        # 9. ADDITIONAL NOTES / FAQ
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("9. Additional Notes / FAQs", id="additional-notes"),
                    html.P([
                        "• For deployment, see ",
                        html.Code("gunicorn_config.py", style=code_style),
                        " with 1 worker and 1 thread by default—adjust as needed for concurrency. ",
                        html.Br(),
                        "• If you see unexpected metrics, confirm that the selected filters (year, portfolio, etc.) match your usage scenario. ",
                        html.Br(),
                        "• For performance concerns, consider adding or adjusting memoization times (",
                        html.Code("flask_caching", style=code_style),
                        ") in ",
                        html.Code("cache.py", style=code_style),
                        "."
                    ]),
                ], className="card info-card fade-in")
            ], width=12)
        ], className="mb-5"),

    ], fluid=True, className="py-4")
