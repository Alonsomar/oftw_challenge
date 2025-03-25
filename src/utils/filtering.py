"""
Funciones optimizadas para filtrar datos en función de criterios definidos.
"""

import pandas as pd

def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filtra un DataFrame basado en un conjunto de filtros optimizados usando query().

    :param df: DataFrame a filtrar.
    :param filters: Diccionario de filtros con formato {"columna": valor}.
    :return: DataFrame filtrado.
    """
    if df.empty:
        return df

    conditions = []
    for col, value in filters.items():
        if col in df.columns:
            if isinstance(value, list) and value:
                conditions.append(f"{col} in {value}")
            elif value is not None:
                conditions.append(f"{col} == '{value}'")

    query_str = " & ".join(conditions)
    return df.query(query_str) if query_str else df

def get_date_ranges_from_years(years, year_mode):
    """
    Dado un array de 'years' (strings o ints) y year_mode (fiscal|calendar),
    devuelve una lista de (start_date, end_date) para cada 'year' seleccionado.
    """
    date_ranges = []
    for y in years:
        y_int = int(y)  # convertir a entero, p.ej '2024' -> 2024

        if year_mode == "fiscal":
            # El "FY 2024" va del 1-Jul-2024 al 30-Jun-2025
            start_dt = pd.Timestamp(year=y_int, month=7, day=1)
            end_dt   = pd.Timestamp(year=y_int+1, month=6, day=30, hour=23, minute=59, second=59)
        else:
            # year_mode == "calendar"
            start_dt = pd.Timestamp(year=y_int, month=1, day=1)
            end_dt   = pd.Timestamp(year=y_int, month=12, day=31, hour=23, minute=59, second=59)

        date_ranges.append((start_dt, end_dt))

    return date_ranges
