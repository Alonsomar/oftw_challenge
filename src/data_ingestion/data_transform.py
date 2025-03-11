import pandas as pd
from data_read import read_data
from log_config import get_logger

logger = get_logger(__name__)

# Definir moneda base y tasas de conversión (valores de ejemplo, deben actualizarse dinámicamente)
CURRENCY_EXCHANGE = {
    "USD": 1,
    "GBP": 1.3,
    "EUR": 1.1,
    "AUD": 0.75,
    "CAD": 0.78
}


def normalize_dates(df: pd.DataFrame, date_columns: list) -> pd.DataFrame:
    """Convierte columnas de fecha al formato datetime."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            logger.info(f"Columna {col} convertida a formato datetime.")
    return df


def convert_currency(df: pd.DataFrame, amount_col: str, currency_col: str) -> pd.DataFrame:
    """Convierte montos a USD usando tasas de conversión predefinidas."""
    if amount_col in df.columns and currency_col in df.columns:
        df["amount_usd"] = df.apply(lambda row: row[amount_col] / CURRENCY_EXCHANGE.get(row[currency_col], 1), axis=1)
        logger.info(f"Montos convertidos a USD en columna 'amount_usd'.")
    return df


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
        df = convert_currency(df, "amount", "currency")
        # df.fillna({"pledge_ended_at": "9999-12-31"}, inplace=True)  # Tratar valores vacíos
        dfs[name] = df
        logger.info(f"Datos limpiados y transformados para {name}.")

    return dfs


def filter_data(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filtra el DataFrame según las condiciones proporcionadas en `filters`.
    Usa `query()` para optimizar el rendimiento cuando sea posible.

    :param df: DataFrame a filtrar
    :param filters: Diccionario con los filtros, ej: {"currency": "USD", "amount_usd__gt": 50}
    :return: DataFrame filtrado
    """
    if df.empty:
        logger.warning("El DataFrame está vacío, no se aplicarán filtros.")
        return df

    conditions = []

    for col, value in filters.items():
        if "__" in col:
            col_name, op = col.split("__")
            if col_name in df.columns:
                if op == "gt":
                    conditions.append(f"`{col_name}` > {value}")
                elif op == "lt":
                    conditions.append(f"`{col_name}` < {value}")
                elif op == "eq":
                    conditions.append(f"`{col_name}` == '{value}'")
        else:
            if col in df.columns:
                conditions.append(f"`{col}` == '{value}'")

    query_str = " & ".join(conditions)
    if query_str:
        df = df.query(query_str)
        logger.info(f"Aplicado filtro: {query_str}")

    return df


if __name__ == "__main__":
    # Cargar y transformar datos
    dfs = read_data()
    transformed_dfs = clean_data(dfs)

    # Ejemplo de filtrado
    sample_filters = {
        "currency": "USD",
        "amount_usd__gt": 100
    }
    filtered_df = filter_data(transformed_dfs["payments"], sample_filters)

    print(filtered_df.head())  # Ver primeros resultados filtrados
