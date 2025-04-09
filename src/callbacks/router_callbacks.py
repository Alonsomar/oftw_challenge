from dash.dependencies import Input, Output
from dash import no_update, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from src.pages.money_moved_layout import money_moved_layout
from src.pages.objectics_layout import objectics_layout
from src.pages.pledge_perf_layout import pledge_perf_layout
from src.pages.home_layout import home_layout
from src.pages.notes import notes_layout
from src.data_ingestion.data_loader import load_clean_data
from src.pages.chat_llm_layout import chat_llm_layout


def register_callbacks(app):
    @app.callback(
        [
            Output("year-filter", "options"),
            Output("portfolio-filter", "options"),
        ],
        [Input("url", "pathname")],  # dispara cuando la url cambia
        prevent_initial_call=True
    )
    def load_data_and_set_dropdowns(pathname):
        """
        Se ejecuta la primera vez que el usuario entra a la app
        (y luego cada vez que cambie la ruta).
        Carga datos al caché y define las opciones en los dropdown.
        """

        # Cargar datos (esto internamente cachea la info)
        dfs = load_clean_data()
        payments_df = dfs.get("payments")
        if payments_df is None or payments_df.empty:
            raise PreventUpdate

        # Asegúrate de tener la columna year convertida (si no, hazlo aquí).
        payments_df["year"] = payments_df["date"].dt.year.astype(str)

        # Construir opciones
        year_opts = [{"label": y, "value": y} for y in sorted(payments_df["year"].unique())]
        portfolio_opts = [
            {"label": p, "value": p}
            for p in sorted(payments_df["portfolio"].dropna().unique())
        ]

        return year_opts, portfolio_opts

    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def display_page(pathname):
        if pathname == "/money_moved":
            return money_moved_layout()
        elif pathname == "/objectics":
            return objectics_layout()
        elif pathname == "/pledge_perf":
            return pledge_perf_layout()
        elif pathname == "/notes":
            return notes_layout()
        elif pathname == "/chat_llm":
            return chat_llm_layout()
        elif pathname == "/" or pathname == "":  # Cuando es la raíz
            return home_layout()
        else:
            # Página 404
            return html.H4("404: Invalid route. Select an option on the sidebar.")

    from src.callbacks.objectics_callbacks import register_objective_callbacks
    from src.callbacks.money_moved_callbacks import register_money_moved_callbacks
    from src.callbacks.pledge_perf_callbacks import register_performance_callbacks
    from src.callbacks.chat_llm_callbacks import register_chat_llm_callbacks

    register_objective_callbacks(app)
    register_money_moved_callbacks(app)
    register_performance_callbacks(app)
    register_chat_llm_callbacks(app)
