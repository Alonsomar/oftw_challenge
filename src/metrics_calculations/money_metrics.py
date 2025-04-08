"""
Calcula las métricas de 'Money Moved' basadas en el dataset de pagos.
"""

import pandas as pd
from src.utils.financial import classify_donation_type
from log_config import get_logger

logger = get_logger(__name__)

EXCLUDED_PORTFOLIOS = [
    "One for the World Discretionary Fund",
    "One for the World Operating Costs"
]

CALENDAR_LABELS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

FISCAL_LABELS = {
    1: "Jul", 2: "Aug", 3: "Sep", 4: "Oct", 5: "Nov", 6: "Dec",
    7: "Jan", 8: "Feb", 9: "Mar", 10: "Apr", 11: "May", 12: "Jun"
}

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
    df_filtered["donation_type"] = df_filtered["frequency"].apply(classify_donation_type)


    # Agrupar Money Moved por tipo de donación
    donation_type_money_moved = df_filtered.groupby("donation_type")["amount_usd"].sum().reset_index()
    logger.info("Calculado Money Moved por tipo de donación.")

    return donation_type_money_moved


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


def calculate_accumulated_money_moved(df: pd.DataFrame, year_mode: str) -> pd.DataFrame:
    """
    Calcula el monto movido de forma acumulada POR AÑO
    (sea fiscal o calendario), retornando un DF para graficar.
    """

    if df.empty:
        return pd.DataFrame()

    # Excluir portfolios no deseados
    df_filtered = df[~df["portfolio"].isin(EXCLUDED_PORTFOLIOS)].copy()

    # Asumiendo que ya has filtrado este DF a un año o varios (en el callback).
    # Aun así, necesitamos "año contable" y "mes contable".
    # Dependerá de year_mode: 'calendar' vs 'fiscal'.

    # 1) Crear col. year y col. month reales
    df_filtered["actual_year"] = df_filtered["date"].dt.year
    df_filtered["month"] = df_filtered["date"].dt.month

    # 2) Crear "contable_year"
    if year_mode == "calendar":
        # contable_year = actual_year
        df_filtered["contable_year"] = df_filtered["actual_year"]
    else:
        # year_mode == "fiscal"
        # Si month >= 7 => contable_year = actual_year
        # Si month < 7  => contable_year = actual_year - 1
        df_filtered["contable_year"] = df_filtered.apply(
            lambda row: row["actual_year"] if row["month"] >= 7 else row["actual_year"] - 1,
            axis=1
        )

    # 3) Agrupar por contable_year, y contable_month para resumir
    # contable_month = 1..12 en orden: 1=Jul, 2=Aug,... si es fiscal?
    #   eso se hace con un offset, si deseas.
    #   O a veces, para graficar, basta con "fecha" ordenada.
    #
    # Ejemplo simple: agrupar por (contable_year, date) => monthly sums
    # luego en plot, mostrar un label year-month.
    # Si quieres un "mes contable" estilo 1..12, se hace un shift.

    # Generemos un "contable_month" sin shift:
    if year_mode == "calendar":
        df_filtered["contable_month"] = df_filtered["month"]
    else:
        # fiscal: mes 7 -> contable_month=1, mes 8 -> 2, ... mes 6->12
        # => contable_month = (month - 7 + 12) % 12 + 1
        df_filtered["contable_month"] = ((df_filtered["month"] - 7) % 12) + 1

    if year_mode == "calendar":
        df_filtered["month_label"] = df_filtered["contable_month"].map(CALENDAR_LABELS)
    else:
        df_filtered["month_label"] = df_filtered["contable_month"].map(FISCAL_LABELS)

    # Sumar amount_usd por contable_year y contable_month
    grouped = df_filtered.groupby(["contable_year", "contable_month"], as_index=False)["amount_usd"].sum()

    # Ordenar
    grouped.sort_values(["contable_year", "contable_month"], inplace=True)

    # Hacer cumsum por contable_year
    grouped["cumulative_usd"] = grouped.groupby("contable_year")["amount_usd"].cumsum()

    # Opcional: generar una col. label p.ej. "FY24 M1" o "2023-01"
    # Depende de si quieres un label unificado
    if year_mode == "calendar":
        # monthly label e.g. "2023-01"
        grouped["year_month_label"] = grouped["contable_year"].astype(str) + "-" + grouped["contable_month"].astype(str)
    else:
        # e.g. "FY24 M3"
        grouped["year_month_label"] = "FY" + grouped["contable_year"].astype(str).str[-2:] + " M" + grouped["contable_month"].astype(str)

    return grouped


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