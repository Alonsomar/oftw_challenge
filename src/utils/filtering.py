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

