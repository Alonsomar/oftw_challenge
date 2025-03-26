from dash.dependencies import Input, Output
from dash import no_update, html
from src.pages.money_moved_layout import money_moved_layout
from src.pages.objectics_layout import objectics_layout
from src.pages.pledge_perf_layout import pledge_perf_layout
from src.pages.home_layout import home_layout

def register_callbacks(app):

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
        elif pathname == "/" or pathname == "":  # Cuando es la raíz
            return home_layout()
        else:
            # Página 404
            return html.H4("404: Invalid route. Select an option on the sidebar.")

    from src.callbacks.objectics_callbacks import register_objective_callbacks
    from src.callbacks.money_moved_callbacks import register_money_moved_callbacks
    from src.callbacks.pledge_perf_callbacks import register_performance_callbacks


    register_objective_callbacks(app)
    register_money_moved_callbacks(app)
    register_performance_callbacks(app)
