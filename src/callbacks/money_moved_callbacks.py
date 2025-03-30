import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved, calculate_money_moved_by_donation_type, calculate_money_moved_by_platform, calculate_money_moved_by_source
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved, plot_money_moved_by_platform, plot_money_moved_by_donation_type, plot_money_moved_treemap


def register_money_moved_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("money-moved-graph", "figure"),
         Output("counterfactual-money-moved-graph", "figure")],
        [Input("store-filtered-data", "data")]
    )
    def update_graphs(filtered_data_json):
        """
        Actualiza los gráficos de Money Moved y Counterfactual Money Moved
        en función de los filtros seleccionados.
        """

        if not filtered_data_json:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return empty_fig, empty_fig

        # Decodificar JSON
        data_dict = json.loads(filtered_data_json)

        # Construir DataFrame
        payments_df = pd.DataFrame(data_dict["payments"])

        # Convertir la(s) columna(s) de fecha a datetime
        # (asumiendo que la columna se llama "date")
        payments_df["date"] = pd.to_datetime(payments_df["date"], format="%Y-%m-%d %H:%M:%S", errors="coerce")

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
        [Input("store-filtered-data", "data")]
    )
    def update_additional_metrics(filtered_data_json):
        """
        Actualiza gráficos de Money Moved por plataforma, por tipo de donación y por fuente.
        """

        if not filtered_data_json:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return empty_fig, empty_fig, empty_fig

        data_dict = json.loads(filtered_data_json)
        payments_df = pd.DataFrame(data_dict["payments"])
        pledges_df = pd.DataFrame(data_dict["pledges"])

        datetime_cols_payments = ["date"]  # o ["date", "some_other_date_col"] si hay más
        for col in datetime_cols_payments:
            if col in payments_df.columns:
                payments_df[col] = pd.to_datetime(payments_df[col], errors="coerce")

        datetime_cols_pledges = ["pledge_created_at", "pledge_starts_at", "pledge_ended_at"]
        for col in datetime_cols_pledges:
            if col in pledges_df.columns:
                pledges_df[col] = pd.to_datetime(pledges_df[col], errors="coerce")

        df_platform = calculate_money_moved_by_platform(payments_df)

        if df_platform.empty:
            fig_platform = go.Figure()
        else:
            fig_platform = plot_money_moved_by_platform(df_platform)

        fig_donation_type = plot_money_moved_by_donation_type(
            calculate_money_moved_by_donation_type(payments_df, pledges_df))

        fig_source = plot_money_moved_treemap(calculate_money_moved_by_source(payments_df, pledges_df))

        return fig_platform, fig_donation_type, fig_source
