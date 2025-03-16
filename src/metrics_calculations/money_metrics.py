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


def calculate_money_moved_by_platform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Money Moved total, agrupado por plataforma de pago.

    :param df: DataFrame de pagos.
    :return: DataFrame con Money Moved por plataforma.
    """
    if df.empty or "payment_platform" not in df.columns or "amount_usd" not in df.columns:
        logger.warning("El DataFrame de pagos está vacío o faltan columnas necesarias.")
        return pd.DataFrame(columns=["payment_platform", "amount_usd"])

    df_filtered = df[~df["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    platform_money_moved = df_filtered.groupby("payment_platform")["amount_usd"].sum().reset_index()

    logger.info("Calculado Money Moved por plataforma.")
    return platform_money_moved

def calculate_money_moved_by_donation_type(payments_df: pd.DataFrame, pledges_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Money Moved separado en donaciones 'One-Time' y 'Recurring',
    basándose en la columna 'frequency' de pledges.

    :param payments_df: DataFrame de pagos.
    :param pledges_df: DataFrame de pledges (para obtener la frecuencia de pago).
    :return: DataFrame con Money Moved por tipo de donación.
    """
    if payments_df.empty or pledges_df.empty:
        logger.warning("Uno de los DataFrames está vacío. No se calculará Money Moved por tipo de donación.")
        return pd.DataFrame()

    # Verificar que 'pledge_id' está en ambos DataFrames
    if "pledge_id" not in payments_df.columns or "pledge_id" not in pledges_df.columns:
        logger.error("No se encontró 'pledge_id' en los DataFrames, no se puede hacer merge.")
        return pd.DataFrame()

    # Unir `payments` con `pledges` en `pledge_id` para obtener la frecuencia
    df_merged = payments_df.merge(pledges_df[['pledge_id', 'frequency']], on='pledge_id', how='left')

    # Filtrar portafolios excluidos
    df_filtered = df_merged[~df_merged["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    # Manejar valores NaN en 'frequency'
    df_filtered.fillna({"frequency": "Unknown"}, inplace=True)

    # Determinar si es Recurring o One-Time
    df_filtered["donation_type"] = df_filtered["frequency"].apply(
        lambda x: "Recurring" if x in ["Monthly", "Annually", "Quarterly"] else "One-Time"
    )

    # Agrupar Money Moved por tipo de donación
    donation_type_money_moved = df_filtered.groupby("donation_type")["amount_usd"].sum().reset_index()
    logger.info("Calculado Money Moved por tipo de donación.")

    return donation_type_money_moved

def calculate_active_arr(df: pd.DataFrame) -> float:
    """
    Calcula el Annualized Run Rate (ARR) de donaciones activas.

    :param df: DataFrame de pledges.
    :return: Active ARR total en USD.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará Active ARR.")
        return 0.0

    active_pledges = df[df["pledge_status"] == "Active donor"].copy()

    # Manejar valores nulos en 'frequency'
    active_pledges["frequency"].fillna("Unknown", inplace=True)

    # Convertir montos a ARR dependiendo de la frecuencia de pago
    def annualize_amount(row):
        if row["frequency"] == "Monthly":
            return row["contribution_amount"] * 12
        elif row["frequency"] == "Quarterly":
            return row["contribution_amount"] * 4
        elif row["frequency"] == "Annually":
            return row["contribution_amount"]
        else:
            return 0  # Omitir pagos no especificados

    active_pledges["annualized_amount"] = active_pledges.apply(annualize_amount, axis=1)

    total_arr = active_pledges["annualized_amount"].sum()
    logger.info(f"Active ARR calculado: ${total_arr:,.2f}")

    return total_arr

def calculate_pledge_attrition_rate(df: pd.DataFrame) -> float:
    """
    Calcula el Pledge Attrition Rate basado en pledges cancelados.

    :param df: DataFrame de pledges.
    :return: Proporción de pledges que han sido cancelados.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará Pledge Attrition Rate.")
        return 0.0

    total_pledges = df.shape[0]
    churned_pledges = df[df["pledge_status"].isin(["Payment failure", "Churned donor"])].shape[0]

    attrition_rate = churned_pledges / total_pledges if total_pledges > 0 else 0.0
    logger.info(f"Pledge Attrition Rate calculado: {attrition_rate:.2%}")

    return attrition_rate


def calculate_money_moved_by_source(payments_df: pd.DataFrame, pledges_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Money Moved por fuente (capítulo de donante y tipo de capítulo).

    :param payments_df: DataFrame de pagos.
    :param pledges_df: DataFrame de pledges.
    :return: DataFrame con Money Moved por fuente.
    """
    if payments_df.empty or pledges_df.empty:
        logger.warning("Uno de los DataFrames está vacío. No se calculará Money Moved por fuente.")
        return pd.DataFrame()

    # Verificar que las columnas necesarias existan antes de hacer merge
    required_columns = {"pledge_id", "donor_chapter", "chapter_type"}
    if not required_columns.issubset(set(pledges_df.columns)):
        logger.error(f"Faltan columnas necesarias en pledges_df: {required_columns - set(pledges_df.columns)}")
        return pd.DataFrame()

    # Merge entre payments y pledges para obtener donor_chapter y chapter_type
    df_merged = payments_df.merge(
        pledges_df[["pledge_id", "donor_chapter", "chapter_type"]],
        on="pledge_id",
        how="left"
    )

    # Filtrar portafolios excluidos
    df_filtered = df_merged[~df_merged["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    # Manejar valores nulos en donor_chapter y chapter_type
    df_filtered.fillna({"donor_chapter": "Unknown",
                        "chapter_type": "Unknown"}, inplace=True)

    # Agrupar por fuente y sumar Money Moved
    money_moved_by_source = df_filtered.groupby(["donor_chapter", "chapter_type"])["amount_usd"].sum().reset_index()

    logger.info("Calculado Money Moved por fuente.")

    return money_moved_by_source



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