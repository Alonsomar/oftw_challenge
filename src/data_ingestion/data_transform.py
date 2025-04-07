import os
from pathlib import Path
import pandas as pd
from src.data_ingestion.data_read import read_data
from currency_converter import CurrencyConverter
from log_config import get_logger
from src.utils.cache import cache
from src.utils.filtering import filter_dataframe
from datetime import date

logger = get_logger(__name__)

# Inicializar el conversor de divisas
data_dir = Path(__file__).parent.parent.parent / 'data'
exchange_rate_path = os.path.join(data_dir, 'eurofxref-hist.csv')
currency_converter = CurrencyConverter(exchange_rate_path,
                                       fallback_on_missing_rate=True,
                                       fallback_on_missing_rate_method='last_known',
                                       fallback_on_wrong_date=True)

def normalize_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Convierte columnas de fecha al formato datetime."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            logger.info(f"Columna {col} convertida a formato datetime.")
    return df


def convert_currency(df: pd.DataFrame, amount_col: str, currency_col: str, date_col: str, generated_col_name: str) -> pd.DataFrame:
    """Convierte montos a USD usando el CurrencyConverterUtil."""
    if amount_col in df.columns and currency_col in df.columns:
        try:
            df[generated_col_name] = df.apply(
                lambda row: currency_converter.convert(row[amount_col],
                                                       row[currency_col],
                                                       "USD",
                                                       date=row[date_col]) if pd.notna(row[amount_col]) and pd.notna(row[currency_col]) and (date(1999,1,4) <= row[date_col].date()) else None,
                axis=1
            )
            logger.info(f"Montos convertidos a USD en columna {generated_col_name}.")
        except Exception as e:
            logger.error(f'Problema transformando {amount_col}  a USD: {e}')
            logger.info(f"Los límites de fechas de conversión son: {currency_converter.bounds['USD']}")
    return df

def normalize_na(df, df_name):
    # --- Unificar notación de NaN, valores vacíos, etc. ---
    if df_name == "pledges":
        # Reemplaza cadenas vacías ("") o "n/a" por None, para luego unificarlas
        df.replace({"donor_chapter": {"": None, "n/a": None},
                    "chapter_type": {"": None, "n/a": None}}, inplace=True)

        # Ahora sí, lo que sea None pasará a "Unknown"
        df["donor_chapter"] = df["donor_chapter"].fillna("Unknown")
        df["chapter_type"] = df["chapter_type"].fillna("Unknown")

    elif df_name == "payments":
        # Igualmente para 'portfolio' y 'payment_platform', si aplica
        df.replace({"portfolio": {"": None, "n/a": None},
                    "payment_platform": {"": None, "n/a": None}}, inplace=True)

        df["portfolio"] = df["portfolio"].fillna("Unknown")
        df["payment_platform"] = df["payment_platform"].fillna("Unknown")

    logger.info(f"Notación NaN unificada para dataset {df_name}.")
    return df


@cache.memoize(timeout=300)
def clean_data(dfs: dict) -> dict:
    """Aplica transformaciones a los DataFrames."""
    if not dfs:
        logger.error("No hay datos para procesar.")
        return {}

    # Columnas de fecha en cada dataset
    date_columns = {
        "pledges": ["pledge_created_at", "pledge_starts_at", "pledge_ended_at"],
        "payments": ["date"]
    }

    # Procesar cada DataFrame
    for name, df in dfs.items():
        df = normalize_dates(df, date_columns.get(name, []))
        df = convert_currency(df, "amount", "currency", "date", "amount_usd")
        df = convert_currency(df, "contribution_amount", "currency", "pledge_starts_at", "contribution_amount_usd")
        df = normalize_na(df, name)
        dfs[name] = df
        logger.info(f"Datos limpiados y transformados para {name}.")

    return dfs


if __name__ == "__main__":
    # Cargar y transformar datos
    dfs = read_data()
    transformed_dfs = clean_data(dfs)

    # Ejemplo de filtrado
    sample_filters = {
        "currency": "USD",
        "amount_usd__gt": 100
    }
    filtered_df = filter_dataframe(transformed_dfs["payments"], sample_filters)

    print(filtered_df.head())  # Ver primeros resultados filtrados
    print(filtered_df.info())
