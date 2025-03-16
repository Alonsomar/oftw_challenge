"""
Calcula métricas relacionadas con Pledge Performance.
"""

import pandas as pd
from log_config import get_logger

logger = get_logger(__name__)

def calculate_all_pledges(df: pd.DataFrame) -> int:
    """
    Calcula el total de pledges (activos + futuros).

    :param df: DataFrame de pledges.
    :return: Número total de pledges.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará el total de pledges.")
        return 0

    total_pledges = df[df["pledge_status"].isin(["Pledged donor", "Active donor"])].shape[0]
    logger.info(f"Total Pledges calculado: {total_pledges}")

    return total_pledges

def calculate_future_pledges(df: pd.DataFrame) -> int:
    """
    Calcula el número de pledges futuros (no activos todavía).

    :param df: DataFrame de pledges.
    :return: Número de pledges futuros.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calcularán los pledges futuros.")
        return 0

    future_pledges = df[df["pledge_status"] == "Pledged donor"].shape[0]
    logger.info(f"Future Pledges calculado: {future_pledges}")

    return future_pledges


def calculate_monthly_attrition_rate(df: pd.DataFrame) -> float:
    """
    Calcula la tasa de pérdida de pledges por mes.

    :param df: DataFrame de pledges.
    :return: Monthly Attrition Rate.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará Monthly Attrition Rate.")
        return 0.0

    df["pledge_ended_at"] = pd.to_datetime(df["pledge_ended_at"], errors="coerce")
    df["pledge_starts_at"] = pd.to_datetime(df["pledge_starts_at"], errors="coerce")

    # Filtrar pledges con fecha de finalización válida
    churned_pledges = df[df["pledge_status"].isin(["Payment failure", "Churned donor"])]
    churned_per_month = churned_pledges.groupby(churned_pledges["pledge_ended_at"].dt.to_period("M")).size()

    # Filtrar pledges activos en cada mes
    active_per_month = df.groupby(df["pledge_starts_at"].dt.to_period("M")).size()

    # Calcular tasa de pérdida mensual
    monthly_attrition = (churned_per_month / active_per_month).fillna(0)

    avg_monthly_attrition = monthly_attrition.mean()
    logger.info(f"Monthly Attrition Rate calculado: {avg_monthly_attrition:.2%}")

    return avg_monthly_attrition

def calculate_breakdown_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el desglose de pledges por tipo de capítulo.

    :param df: DataFrame de pledges.
    :return: DataFrame con breakdown de pledges.
    """
    if df.empty:
        logger.warning("El DataFrame de pledges está vacío. No se calculará breakdown por canal.")
        return pd.DataFrame()

    breakdown = df.groupby("chapter_type")["pledge_id"].count().reset_index()
    breakdown.rename(columns={"pledge_id": "pledge_count"}, inplace=True)

    logger.info("Breakdown por canal calculado.")
    return breakdown
