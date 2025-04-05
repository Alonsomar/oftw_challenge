import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved, calculate_money_moved_by_donation_type, calculate_money_moved_by_platform, calculate_money_moved_by_source
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved, plot_money_moved_by_platform, plot_money_moved_by_donation_type, plot_money_moved_treemap
from src.utils.callbacks_filter import get_filtered_data

def register_money_moved_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("money-moved-graph", "figure"),
         Output("counterfactual-money-moved-graph", "figure")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value"),
         Input("year-mode", "value")]
    )
    def update_graphs(selected_years, selected_portfolios, year_mode):
        """
        Actualiza los gráficos de Money Moved y Counterfactual Money Moved
        en función de los filtros seleccionados.
        """

        payments_df, pledges_df = get_filtered_data(selected_years, selected_portfolios, year_mode)

        if payments_df is None or payments_df.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return empty_fig, empty_fig

        # Calcular métricas
        monthly_money_moved, total_money_moved = calculate_money_moved(payments_df)
        monthly_counterfactual_money_moved, total_counterfactual_money_moved = calculate_counterfactual_money_moved(payments_df)

        # Generar gráficos
        fig1 = plot_money_moved(monthly_money_moved, total_money_moved)
        fig2 = plot_counterfactual_money_moved(monthly_counterfactual_money_moved, total_counterfactual_money_moved)

        return fig1, fig2

    @app.callback(
        [Output("money-moved-platform-graph", "figure"),
         Output("money-moved-donation-type-graph", "figure"),
         Output("money-moved-source-graph", "figure")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value"),
         Input("year-mode", "value")]
    )
    def update_additional_metrics(selected_years, selected_portfolios, year_mode):
        """
        Actualiza gráficos de Money Moved por plataforma, por tipo de donación y por fuente.
        """

        payments_df, pledges_df = get_filtered_data(selected_years, selected_portfolios, year_mode)

        if payments_df is None or payments_df.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return empty_fig, empty_fig, empty_fig

        df_platform = calculate_money_moved_by_platform(payments_df)

        if df_platform.empty:
            fig_platform = go.Figure()
        else:
            fig_platform = plot_money_moved_by_platform(df_platform)

        fig_donation_type = plot_money_moved_by_donation_type(
            calculate_money_moved_by_donation_type(payments_df, pledges_df))

        fig_source = plot_money_moved_treemap(calculate_money_moved_by_source(payments_df, pledges_df))

        return fig_platform, fig_donation_type, fig_source
