"""
Calcula métricas relacionadas con Objectives and Key Results (OKRs).
"""

import pandas as pd
from log_config import get_logger

logger = get_logger(__name__)

def calculate_active_arr(df: pd.DataFrame) -> float:
    """
    Calcula el Active Annualized Run Rate (ARR) basado en pledges activos.

    :param df: DataFrame de pledges.
    :return: Active ARR total en USD.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará Active ARR.")
        return 0.0

    active_pledges = df[df["pledge_status"] == "Active donor"].copy()

    # Manejar valores nulos en 'frequency'
    active_pledges.fillna({"frequency": "Unknown"}, inplace=True)

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

def calculate_total_active_donors(df: pd.DataFrame) -> int:
    """
    Calcula el total de donantes activos.

    :param df: DataFrame de pledges.
    :return: Número de donantes únicos activos.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará el número de donantes activos.")
        return 0

    active_donors = df[df["pledge_status"].isin(["One-time donor", "Active donor"])]["donor_id"].nunique()
    logger.info(f"Total Active Donors calculado: {active_donors}")

    return active_donors

def calculate_total_active_pledges(df: pd.DataFrame) -> int:
    """
    Calcula el total de pledges activos.

    :param df: DataFrame de pledges.
    :return: Número de pledges activos.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará el número de pledges activos.")
        return 0

    active_pledges = df[df["pledge_status"] == "Active donor"].shape[0]
    logger.info(f"Total Active Pledges calculado: {active_pledges}")

    return active_pledges

def calculate_chapter_arr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el ARR por tipo de capítulo.

    :param df: DataFrame de pledges.
    :return: DataFrame con el ARR por chapter_type.
    """
    if df.empty or "chapter_type" not in df.columns or "contribution_amount" not in df.columns:
        logger.warning("El DataFrame de pledges está vacío o faltan columnas necesarias. Se devolverá un DataFrame vacío.")
        return pd.DataFrame(columns=["chapter_type", "ARR_USD"])

    active_pledges = df[df["pledge_status"] == "Active donor"].copy()
    active_pledges.fillna({"frequency": "Unknown"}, inplace=True)

    def annualize_amount(row):
        if row["frequency"] == "Monthly":
            return row["contribution_amount"] * 12
        elif row["frequency"] == "Quarterly":
            return row["contribution_amount"] * 4
        elif row["frequency"] == "Annually":
            return row["contribution_amount"]
        else:
            return 0

    active_pledges["annualized_amount"] = active_pledges.apply(annualize_amount, axis=1)

    chapter_arr = active_pledges.groupby("chapter_type")["annualized_amount"].sum().reset_index()
    chapter_arr.rename(columns={"annualized_amount": "ARR_USD"}, inplace=True)

    logger.info("Chapter ARR calculado correctamente.")
    return chapter_arr
