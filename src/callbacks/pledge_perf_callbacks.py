import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.metrics_calculations.performance_metrics import calculate_all_pledges, calculate_future_pledges, calculate_breakdown_by_channel, calculate_monthly_attrition_rate
from src.metrics_vizualizations.performance_viz import plot_breakdown_by_channel
from src.utils.financial import calculate_arr


def register_performance_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("total-pledges", "children"),
         Output("future-pledges", "children"),
         Output("all-arr", "children"),
         Output("future-arr", "children"),  # NUEVO
         Output("active-arr", "children"),  # NUEVO
         Output("monthly-attrition-rate", "children"),
         Output("breakdown-channel-graph", "figure")],
        [Input("store-filtered-data", "data")]
    )
    def update_performance_metrics(filtered_data_json):

        if not filtered_data_json:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", empty_fig

        data_dict = json.loads(filtered_data_json)
        pledges_df = pd.DataFrame(data_dict["pledges"])

        datetime_cols_pledges = ["pledge_created_at", "pledge_starts_at", "pledge_ended_at"]
        for col in datetime_cols_pledges:
            if col in pledges_df.columns:
                pledges_df[col] = pd.to_datetime(pledges_df[col], errors="coerce")


        # Calcular las métricas
        total_pledges_val = calculate_all_pledges(pledges_df)
        future_pledges_val = calculate_future_pledges(pledges_df)
        all_arr_val = calculate_arr(pledges_df, ["Pledged donor", "Active donor"])
        future_arr_val = calculate_arr(pledges_df, ["Pledged donor"])
        active_arr_val = calculate_arr(pledges_df, ["Active donor"])
        monthly_attrition_val = calculate_monthly_attrition_rate(pledges_df)
        breakdown_fig = plot_breakdown_by_channel(calculate_breakdown_by_channel(pledges_df))

        return (
            total_pledges_val,
            future_pledges_val,
            f"${all_arr_val:,.2f}",
            f"${future_arr_val:,.2f}",  # Future ARR en formato $
            f"${active_arr_val:,.2f}",  # Active ARR en formato $
            f"{monthly_attrition_val * 100:.2f}%",
            breakdown_fig
        )
