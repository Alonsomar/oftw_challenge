import plotly.graph_objects as go
from dash.dependencies import Input, Output
from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import filter_dataframe, get_date_ranges_from_years
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved, calculate_money_moved_by_donation_type, calculate_money_moved_by_platform, calculate_money_moved_by_source
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved, plot_money_moved_by_platform, plot_money_moved_by_donation_type, plot_money_moved_treemap


def register_money_moved_callbacks(app):
    """
    Registra los callbacks en la aplicación Dash.
    """

    @app.callback(
        [Output("money-moved-graph", "figure"),
         Output("counterfactual-money-moved-graph", "figure"),
         Output("year-filter", "options"),
         Output("portfolio-filter", "options")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value"),
         Input("year-mode", "value")]
    )
    def update_graphs(selected_years, selected_portfolios, year_mode):
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
        if selected_portfolios:
            filters["portfolio"] = selected_portfolios

        # 1) Calcular date ranges
        if selected_years:
            date_ranges = get_date_ranges_from_years(selected_years, year_mode)
            # date_ranges es, por ej, [(Timestamp(2024-07-01), Timestamp(2025-06-30))]
        else:
            date_ranges = []

        # 2) Filtrar payments_df por esos rangos
        if date_ranges:
            # filtrar por OR de todos esos rangos
            mask = False
            for (start_dt, end_dt) in date_ranges:
                mask |= (payments_df["date"] >= start_dt) & (payments_df["date"] <= end_dt)
            filtered_df = filter_dataframe(payments_df[mask], filters)
        else:
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
