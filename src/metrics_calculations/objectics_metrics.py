"""
Calcula métricas relacionadas con Objectives and Key Results (OKRs).
"""

import pandas as pd
from src.utils.financial import calculate_arr
from log_config import get_logger

logger = get_logger(__name__)


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


def calculate_chapter_arr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el ARR por tipo de capítulo.
    """
    if df.empty or "chapter_type" not in df.columns or "contribution_amount" not in df.columns:
        logger.warning("El DataFrame de pledges está vacío o faltan columnas necesarias.")
        return pd.DataFrame(columns=["chapter_type", "ARR_USD"])

    chapter_arr = df.groupby("chapter_type").apply(lambda x: calculate_arr(x, ["Active donor"])).reset_index()
    chapter_arr.rename(columns={0: "ARR_USD"}, inplace=True)

    logger.info("Chapter ARR calculado correctamente.")
    return chapter_arr

