import json
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.metrics_calculations.objectics_metrics import calculate_chapter_arr, calculate_total_active_donors
from src.metrics_vizualizations.objectics_viz import plot_chapter_arr
from src.utils.financial import calculate_pledge_attrition_rate
from src.utils.callbacks_filter import get_filtered_data


def register_objective_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("total-active-donors", "children"),
         Output("total-active-pledges", "children"),
         Output("pledge-attrition-rate", "children"),
         Output("chapter-arr-graph", "figure")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value"),
         Input("year-mode", "value")]
    )
    def update_objectives_metrics(selected_years, selected_portfolios, year_mode):

        payments_df, pledges_df = get_filtered_data(selected_years, selected_portfolios, year_mode)

        if pledges_df is None or pledges_df.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return "N/A", "N/A", "N/A", empty_fig

        chapter_arr_df = calculate_chapter_arr(pledges_df)

        if chapter_arr_df.empty:
            fig_chapter_arr = go.Figure()
        else:
            fig_chapter_arr = plot_chapter_arr(chapter_arr_df)

        return (calculate_total_active_donors(pledges_df),
                pledges_df[pledges_df["pledge_status"] == "Active donor"][
                    "donor_id"
                ].nunique(),
                f"{calculate_pledge_attrition_rate(pledges_df) * 100:.2f}%",
                fig_chapter_arr)