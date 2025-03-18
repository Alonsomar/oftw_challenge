import os
from pathlib import Path
import pandas as pd
from src.data_ingestion.data_read import read_data
from currency_converter import CurrencyConverter
from log_config import get_logger
from src.utils.cache import cache
from src.utils.filtering import filter_dataframe

logger = get_logger(__name__)

# Inicializar el conversor de divisas
data_dir = Path(__file__).parent.parent.parent / 'data'
exchange_rate_path = os.path.join(data_dir, 'eurofxref-hist.csv')
currency_converter = CurrencyConverter(exchange_rate_path,
                                       fallback_on_missing_rate=True,
                                       fallback_on_missing_rate_method='last_known')

def normalize_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Convierte columnas de fecha al formato datetime."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            logger.info(f"Columna {col} convertida a formato datetime.")
    return df


def convert_currency(df: pd.DataFrame, amount_col: str, currency_col: str, date_col: str) -> pd.DataFrame:
    """Convierte montos a USD usando el CurrencyConverterUtil."""
    if amount_col in df.columns and currency_col in df.columns:
        try:
            df["amount_usd"] = df.apply(
                lambda row: currency_converter.convert(row[amount_col],
                                                       row[currency_col],
                                                       "USD",
                                                       date=row[date_col]) if pd.notna(row[amount_col]) and pd.notna(row[currency_col]) else None,
                axis=1
            )
            logger.info(f"Montos convertidos a USD en columna 'amount_usd'.")
        except Exception as e:
            logger.error(f'Problema transformando los datos a USD: {e}')
            logger.info(f'Los límites de fechas de conversión son: {currency_converter.bounds['USD']}')
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
        df = convert_currency(df, "amount", "currency", "date")
        # df.fillna({"pledge_ended_at": "9999-12-31"}, inplace=True)  # Tratar valores vacíos
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
