"""
Define los callbacks para actualizar los gráficos dinámicamente según los filtros seleccionados.
"""

import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import filter_dataframe
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved, calculate_money_moved_by_donation_type, calculate_money_moved_by_platform, calculate_money_moved_by_source
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved, plot_money_moved_by_platform, plot_money_moved_by_donation_type, plot_money_moved_treemap
from src.metrics_calculations.objectics_metrics import calculate_chapter_arr, calculate_total_active_donors
from src.metrics_vizualizations.objectics_viz import plot_chapter_arr
from src.metrics_calculations.performance_metrics import calculate_all_pledges, calculate_future_pledges, calculate_breakdown_by_channel, calculate_monthly_attrition_rate
from src.metrics_vizualizations.performance_viz import plot_breakdown_by_channel
from src.utils.financial import calculate_pledge_attrition_rate, calculate_arr


def register_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("money-moved-graph", "figure"),
         Output("counterfactual-money-moved-graph", "figure"),
         Output("year-filter", "options"),
         Output("portfolio-filter", "options")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value")]
    )
    def update_graphs(selected_years, selected_portfolios):
        """
        Actualiza los gráficos de Money Moved y Counterfactual Money Moved
        en función de los filtros seleccionados.
        """

        # Cargar y limpiar datos
        dfs = load_clean_data()
        payments_df = dfs.get("payments", None)

        if payments_df is None or payments_df.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(text="No Data Available", showarrow=False, x=0.5, y=0.5, xref="paper",
                                     yref="paper")
            return empty_fig, empty_fig, [], []

        # Convertir fecha a formato adecuado para filtrado
        payments_df["year"] = payments_df["date"].dt.year.astype(str)

        # Crear filtros
        filters = {}
        if selected_years:
            filters["year"] = selected_years
        if selected_portfolios:
            filters["portfolio"] = selected_portfolios

        # Aplicar filtros
        filtered_df = filter_dataframe(payments_df, filters)

        # Calcular métricas
        monthly_money_moved, total_money_moved = calculate_money_moved(filtered_df)
        monthly_counterfactual_money_moved, total_counterfactual_money_moved = calculate_counterfactual_money_moved(filtered_df)

        # Generar gráficos
        fig1 = plot_money_moved(monthly_money_moved, total_money_moved)
        fig2 = plot_counterfactual_money_moved(monthly_counterfactual_money_moved, total_counterfactual_money_moved)

        # Extraer valores únicos para dropdowns
        year_options = [{"label": year, "value": year} for year in sorted(payments_df["year"].unique())]
        portfolio_options = [{"label": p, "value": p} for p in sorted(payments_df["portfolio"].dropna().unique())]

        return fig1, fig2, year_options, portfolio_options

    @app.callback(
        [Output("money-moved-platform-graph", "figure"),
         Output("money-moved-donation-type-graph", "figure"),
         Output("money-moved-source-graph", "figure")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value")]
    )
    def update_additional_metrics(selected_years, selected_portfolios):
        """
        Actualiza gráficos de Money Moved por plataforma, por tipo de donación y por fuente.
        """

        dfs = load_clean_data()
        payments_df = dfs.get("payments", None)
        pledges_df = dfs.get("pledges", None)

        if payments_df is None or payments_df.empty or pledges_df is None or pledges_df.empty:
            return {}, {}, {}

        filters = {}
        if selected_years:
            filters["year"] = selected_years
        if selected_portfolios:
            filters["portfolio"] = selected_portfolios

        filtered_df = filter_dataframe(payments_df, filters)

        df_platform = calculate_money_moved_by_platform(filtered_df)

        if df_platform.empty:
            fig_platform = go.Figure()
        else:
            fig_platform = plot_money_moved_by_platform(df_platform)

        fig_donation_type = plot_money_moved_by_donation_type(
            calculate_money_moved_by_donation_type(filtered_df, pledges_df))

        fig_source = plot_money_moved_treemap(calculate_money_moved_by_source(filtered_df, pledges_df))

        return fig_platform, fig_donation_type, fig_source

    @app.callback(
        [Output("total-active-donors", "children"),
         Output("total-active-pledges", "children"),
         Output("pledge-attrition-rate", "children"),
         Output("chapter-arr-graph", "figure")],
        [Input("year-filter", "value")]
    )
    def update_objectives_metrics(selected_years):
        pledges_df = load_clean_data().get("pledges", None)
        if pledges_df is None or pledges_df.empty:
            return "N/A", "N/A", "N/A", go.Figure()

        chapter_arr_df = calculate_chapter_arr(pledges_df)

        if chapter_arr_df.empty:
            fig_chapter_arr = go.Figure()
        else:
            fig_chapter_arr = plot_chapter_arr(chapter_arr_df)

        return (calculate_total_active_donors(pledges_df),
                pledges_df[pledges_df["pledge_status"] == "Active donor"].shape[0],
                f"{calculate_pledge_attrition_rate(pledges_df) * 100:.2f}%",
                fig_chapter_arr)

    @app.callback(
        [Output("total-pledges", "children"),
         Output("future-pledges", "children"),
         Output("all-arr", "children"),
         Output("monthly-attrition-rate", "children"),
         Output("breakdown-channel-graph", "figure")],
        [Input("year-filter", "value")]
    )
    def update_performance_metrics(selected_years):
        pledges_df = load_clean_data().get("pledges", None)
        if pledges_df is None or pledges_df.empty:
            return "N/A", "N/A", "N/A", "N/A", go.Figure()

        return (calculate_all_pledges(pledges_df),
                calculate_future_pledges(pledges_df),
                f"${calculate_arr(pledges_df, ["Pledged donor", "Active donor"]):,.2f}",
                f"{calculate_monthly_attrition_rate(pledges_df) * 100:.2f}%",
                plot_breakdown_by_channel(calculate_breakdown_by_channel(pledges_df)))
