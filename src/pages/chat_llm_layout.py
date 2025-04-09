# src/pages/chat_llm_layout.py

import dash_bootstrap_components as dbc
from dash import html, dcc


def chat_llm_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2("Mini Chat LLM", className="mb-3"),
                    html.P("Ask any questions you want about the filtered data and get contextualized answers."),

                    # Área de texto para la pregunta
                    dcc.Textarea(
                        id="chat-llm-input",
                        placeholder="Write your question here...",
                        style={"width": "100%", "height": "80px"}
                    ),

                    # Botón para enviar la pregunta
                    dbc.Button(
                        "Send",
                        id="chat-llm-submit",
                        color="primary",
                        className="mt-2"
                    ),

                    # Contenedor donde se mostrará la respuesta
                    dcc.Loading(
                        id="chat-llm-loading",
                        type="default",
                        children=[
                            dcc.Markdown(
                                id="chat-llm-response",
                                style={
                                    "marginTop": "1rem",
                                    "whiteSpace": "pre-wrap"
                                }
                            )
                        ]
                    )

                ], className="card p-3")
            ], width=12)
        ])
    ], fluid=True, className="py-4")
