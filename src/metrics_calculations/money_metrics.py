"""
Calcula las métricas de 'Money Moved' basadas en el dataset de pagos.
"""

import pandas as pd
from log_config import get_logger

logger = get_logger(__name__)

EXCLUDED_PORTFOLIOS = [
    "One for the World Discretionary Fund",
    "One for the World Operating Costs"
]


def calculate_money_moved(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el total de dinero movido excluyendo ciertos valores del portfolio.

    :param df: DataFrame de pagos.
    :return: DataFrame con Money Moved agregado por mes y total.
    """
    if df.empty:
        logger.warning("El DataFrame de pagos está vacío. No se calculará Money Moved.")
        return pd.DataFrame()

    # Filtrar portafolios excluidos
    df_filtered = df[~df["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    # Convertir fechas a formato datetime si no están en formato adecuado
    if not pd.api.types.is_datetime64_any_dtype(df_filtered["date"]):
        df_filtered["date"] = pd.to_datetime(df_filtered["date"], errors="coerce")

    # Calcular Money Moved por mes
    # Convertir `Period` a `str` para evitar errores con Plotly
    df_filtered["year_month"] = df_filtered["date"].dt.to_period("M").astype(str)

    monthly_money_moved = df_filtered.groupby("year_month")["amount_usd"].sum().reset_index()

    # Calcular Money Moved total
    total_money_moved = df_filtered["amount_usd"].sum()

    logger.info(f"Money Moved total: ${total_money_moved:,.2f}")

    return monthly_money_moved, total_money_moved


def calculate_counterfactual_money_moved(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el Money Moved contrafactual basado en la columna 'counterfactuality'.

    :param df: DataFrame de pagos.
    :return: DataFrame con Money Moved contrafactual por mes y total.
    """
    if df.empty:
        logger.warning("El DataFrame de pagos está vacío. No se calculará Money Moved contrafactual.")
        return pd.DataFrame()

    # Filtrar portafolios excluidos
    df_filtered = df[~df["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    # Convertir fechas a formato datetime si no están en formato adecuado
    if not pd.api.types.is_datetime64_any_dtype(df_filtered["date"]):
        df_filtered["date"] = pd.to_datetime(df_filtered["date"], errors="coerce")

    # Aplicar el factor contrafactual
    df_filtered["counterfactual_amount"] = df_filtered["amount_usd"] * df_filtered["counterfactuality"]

    # Calcular Money Moved contrafactual por mes
    # Convertir `Period` a `str` para evitar errores con Plotly
    df_filtered["year_month"] = df_filtered["date"].dt.to_period("M").astype(str)

    monthly_counterfactual_money_moved = df_filtered.groupby("year_month")["counterfactual_amount"].sum().reset_index()

    # Calcular Money Moved contrafactual total
    total_counterfactual_money_moved = df_filtered["counterfactual_amount"].sum()

    logger.info(f"Money Moved contrafactual total: ${total_counterfactual_money_moved:,.2f}")

    return monthly_counterfactual_money_moved, total_counterfactual_money_moved


if __name__ == "__main__":
    from src.data_ingestion.data_read import read_data
    from src.data_ingestion.data_transform import clean_data

    # Cargar y transformar datos
    dfs = read_data()
    transformed_dfs = clean_data(dfs)

    # Obtener pagos
    payments_df = transformed_dfs.get("payments", pd.DataFrame())

    # Calcular métricas
    monthly_money_moved, total_money_moved = calculate_money_moved(payments_df)
    monthly_counterfactual_money_moved, total_counterfactual_money_moved = calculate_counterfactual_money_moved(
        payments_df)

    # Imprimir resultados
    print("\n--- Money Moved (Mensual) ---")
    print(monthly_money_moved.head())

    print(f"\nTotal Money Moved: ${total_money_moved:,.2f}")

    print("\n--- Money Moved Contrafactual (Mensual) ---")
    print(monthly_counterfactual_money_moved.head())

    print(f"\nTotal Counterfactual Money Moved: ${total_counterfactual_money_moved:,.2f}")
