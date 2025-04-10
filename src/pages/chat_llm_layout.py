import dash_bootstrap_components as dbc
from dash import html, dcc


def chat_llm_layout():
    return dbc.Container([
        # Header Section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Mini Chat LLM", className="display-4 text-center mb-3 fade-in"),
                    html.P(
                        "Ask any questions you want about the filtered data and get contextualized answers.",
                        className="lead text-center mb-5 fade-in"
                    )
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-5"),

        # Chat Interface
        dbc.Row([
            dbc.Col([
                html.Div([

                    # Envolvemos el contenedor de mensajes en un dcc.Loading
                    dcc.Loading(
                        id="chat-llm-loading",
                        type="circle",  # o "circle", "dot", etc.
                        overlay_style={"visibility": "visible", "filter": "blur(2px)"},
                        children=[
                            html.Div(
                                id="chat-messages-container",
                                className="chat-messages-container mb-4",
                                style={
                                    "height": "400px",
                                    "overflowY": "auto",
                                    "padding": "1rem",
                                    "borderRadius": "var(--border-radius)",
                                    "backgroundColor": "var(--background-card)",
                                    "boxShadow": "var(--shadow-light)"
                                }
                            )
                        ],
                    ),

                    # Input Area
                    html.Div([
                        dcc.Textarea(
                            id="chat-llm-input",
                            placeholder="Write your question here...",
                            className="chat-input",
                            style={
                                "width": "100%",
                                "height": "100px",
                                "padding": "1rem",
                                "borderRadius": "var(--border-radius)",
                                "border": "1px solid var(--border-color)",
                                "resize": "none",
                                "fontFamily": "var(--font-family)",
                                "fontSize": "var(--font-size-base)",
                                "transition": "all var(--transition-normal)"
                            }
                        ),
                        html.Div([
                            dbc.Button(
                                [
                                    html.I(className="fas fa-paper-plane me-2"),
                                    "Send"
                                ],
                                id="chat-llm-submit",
                                color="primary",
                                className="mt-3 chat-submit-button",
                                style={
                                    "background": "var(--gradient-primary)",
                                    "border": "none",
                                    "borderRadius": "30px",
                                    "padding": "0.5rem 2rem",
                                    "fontWeight": "600",
                                    "boxShadow": "var(--shadow-light)",
                                    "transition": "all var(--transition-normal)"
                                }
                            )
                        ], className="text-end")
                    ], className="chat-input-container")
                ], className="card p-4 fade-in")
            ], width=12)
        ])
    ], fluid=True, className="py-4")
