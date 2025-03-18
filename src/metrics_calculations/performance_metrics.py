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
    Calcula la tasa de pérdida de pledges por mes de forma más realista:
      churn_rate(M) = ( pledges que terminan en M ) / ( pledges que estaban activos durante M )
    """
    if df.empty:
        return 0.0

    df = df.copy()  # Para no alterar el original
    df["pledge_starts_at"] = pd.to_datetime(df["pledge_starts_at"], errors="coerce")
    df["pledge_ended_at"] = pd.to_datetime(df["pledge_ended_at"], errors="coerce")

    # Opcional: podríamos excluir “One-time donor” si no queremos que entren al churn
    # df = df[~(df["pledge_status"] == "One-time donor")].copy()

    # Generamos un rango de meses desde la más antigua pledge_starts_at hasta la más reciente pledge_ended_at
    min_month = df["pledge_starts_at"].min().to_period("M")
    max_month = df["pledge_ended_at"].max().to_period("M") if df["pledge_ended_at"].notna().any() else pd.Period.now("M")

    if pd.isna(min_month) or pd.isna(max_month):
        # No hay datos de fechas
        return 0.0

    monthly_churn_rates = []

    # Recorremos cada mes en el rango
    current_month = min_month
    while current_month <= max_month:
        # pledges activas en current_month → pledges que:
        # - tienen pledge_starts_at <= fin del current_month
        # - no terminaron antes de comienzo de current_month
        month_start = current_month.to_timestamp()
        month_end   = (current_month + 1).to_timestamp() - pd.Timedelta("1ns")  # fin del mes

        # Activos = starts_at <= month_end AND (ended_at >= month_start OR ended_at is null)
        # Nota: pledges que no tienen pledge_ended_at => ended_at is null => consideramos que siguen activos
        active_mask = (
            (df["pledge_starts_at"] <= month_end) &
            (
                df["pledge_ended_at"].isna() |
                (df["pledge_ended_at"] >= month_start)
            )
        )
        active_this_month = df[active_mask]

        # Churn en este mes = pledges que cambian a Payment failure/Churned donor con ended_at en [month_start, month_end]
        churn_mask = (
            df["pledge_status"].isin(["Payment failure", "Churned donor"]) &
            (df["pledge_ended_at"] >= month_start) &
            (df["pledge_ended_at"] <= month_end)
        )
        churned_this_month = df[churn_mask]

        n_active = len(active_this_month)
        n_churned = len(churned_this_month)
        churn_rate = n_churned / n_active if n_active > 0 else 0.0

        monthly_churn_rates.append(churn_rate)
        current_month += 1  # pasar al siguiente mes

    # Devolvemos el promedio de churn
    if monthly_churn_rates:
        return float(pd.Series(monthly_churn_rates).mean())
    else:
        return 0.0

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
