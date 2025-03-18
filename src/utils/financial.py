"""
utils/financial.py

Módulo de utilidades financieras y cálculos de métricas compartidas.
"""

import pandas as pd
from log_config import get_logger

logger = get_logger(__name__)

def annualize_amount(frequency: str, amount: float) -> float:
    """
    Convierte montos de contribución en valores anuales según la frecuencia.

    :param frequency: Frecuencia del pledge (Monthly, Quarterly, Annually).
    :param amount: Monto de la contribución.
    :return: Monto anualizado.
    """
    if frequency == "Monthly":
        return amount * 12
    elif frequency == "Quarterly":
        return amount * 4
    elif frequency == "Annually":
        return amount
    else:
        return 0


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
    active_pledges.fillna({"frequency": "Unknown"}, inplace=True)

    active_pledges["annualized_amount"] = active_pledges.apply(
        lambda row: annualize_amount(row["frequency"], row["contribution_amount"]), axis=1
    )

    total_arr = active_pledges["annualized_amount"].sum()
    logger.info(f"Active ARR calculado: ${total_arr:,.2f}")

    return total_arr


def calculate_pledge_attrition_rate(df: pd.DataFrame) -> float:
    """
    Cálculo global de churn:
     - Excluye one-time donors si se desea.
     - Toma todos los pledges con estados de recurrente (Active, Pledged, Payment failure, Churned).
     - El ratio es (# que están en Payment failure o Churned) / (total pledges recurrentes).
    """
    if df.empty:
        return 0.0

    # OPCIONAL: excluir one-time donors
    df = df[df["pledge_status"] != "One-time donor"].copy()

    relevant_statuses = ["Active donor", "Pledged donor","Payment failure","Churned donor"]
    df_relevant = df[df["pledge_status"].isin(relevant_statuses)].copy()

    total_pledges = df_relevant["pledge_id"].nunique()
    churned_pledges = df_relevant[df_relevant["pledge_status"].isin(["Payment failure","Churned donor"])]["pledge_id"].nunique()

    if total_pledges == 0:
        return 0.0

    attrition_rate = churned_pledges / total_pledges
    logger.info(f"Global Pledge Attrition Rate = {attrition_rate:.2%}")
    return attrition_rate


def calculate_arr(df: pd.DataFrame, status_filter: list = None) -> float:
    """
    Calcula el ARR total o filtrado por estados específicos.

    :param df: DataFrame de pledges.
    :param status_filter: Lista opcional con los estados de pledges a incluir.
    :return: ARR total en USD.
    """
    if df.empty:
        return 0.0

    if status_filter:
        df = df[df["pledge_status"].isin(status_filter)]

    # Verificar valores desconocidos en `frequency`
    valid_frequencies = {"Monthly", "Quarterly", "Annually"}
    unexpected_frequencies = set(df["frequency"].dropna().unique()) - valid_frequencies

    if unexpected_frequencies:
        logger.warning(f"Valores inesperados en frequency: {unexpected_frequencies}")

    frequency_map = {
        "Monthly": 12,
        "Quarterly": 4,
        "Annually": 1
    }

    df["annualized_amount"] = df["frequency"].map(frequency_map).fillna(0) * df["contribution_amount"]

    return df["annualized_amount"].sum()



def classify_donation_type(frequency: str) -> str:
    """
    Clasifica una donación como 'Recurring' o 'One-Time' según su frecuencia.

    :param frequency: Frecuencia de la donación.
    :return: 'Recurring' o 'One-Time'.
    """
    return "Recurring" if frequency in ["Monthly", "Annually", "Quarterly"] else "One-Time"
