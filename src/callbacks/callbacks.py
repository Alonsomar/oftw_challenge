"""
Define los callbacks para actualizar los gráficos dinámicamente según los filtros seleccionados.
"""

from dash.dependencies import Input, Output
from src.data_ingestion.data_loader import load_clean_data
from src.utils.filtering import filter_dataframe
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved
from src.metrics_vizualizations.money_viz import plot_money_moved, plot_counterfactual_money_moved

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
