import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.data_ingestion.data_loader import load_clean_data
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
        [Input("year-filter", "value")]
    )
    def update_performance_metrics(selected_years):
        pledges_df = load_clean_data().get("pledges", None)
        if pledges_df is None or pledges_df.empty:
            # Ajustamos para devolver 7 elementos:
            return ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", go.Figure())

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
