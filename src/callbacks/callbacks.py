"""
Define los callbacks para actualizar los gráficos dinámicamente según los filtros seleccionados.
"""

from dash.dependencies import Input, Output
from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import filter_dataframe
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved, calculate_money_moved_by_donation_type, calculate_money_moved_by_platform,calculate_active_arr, calculate_pledge_attrition_rate
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved, plot_money_moved_by_platform, plot_money_moved_by_donation_type

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
            return {}, {}, [], []

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
         Output("money-moved-donation-type-graph", "figure")],
        [Input("year-filter", "value"),
         Input("portfolio-filter", "value")]
    )
    def update_additional_metrics(selected_years, selected_portfolios):
        """
        Actualiza gráficos de Money Moved por plataforma y por tipo de donación.
        """

        dfs = load_clean_data()
        payments_df = dfs.get("payments", None)
        pledges_df = dfs.get("pledges", None)  # Se obtiene pledges_df para obtener `frequency`

        if payments_df is None or payments_df.empty or pledges_df is None or pledges_df.empty:
            return {}, {}

        filters = {}
        if selected_years:
            filters["year"] = selected_years
        if selected_portfolios:
            filters["portfolio"] = selected_portfolios

        filtered_df = filter_dataframe(payments_df, filters)

        # Corrección: solo pasamos filtered_df a la función de visualización
        fig_platform = plot_money_moved_by_platform(calculate_money_moved_by_platform(filtered_df))

        # Corrección: `calculate_money_moved_by_donation_type()` usa `pledges_df`
        donation_type_data = calculate_money_moved_by_donation_type(filtered_df, pledges_df)
        fig_donation_type = plot_money_moved_by_donation_type(donation_type_data)

        return fig_platform, fig_donation_type
