"""
Funciones optimizadas para filtrar datos en función de criterios definidos.
"""

import pandas as pd

def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filtra un DataFrame basado en un conjunto de filtros.

    :param df: DataFrame a filtrar.
    :param filters: Diccionario de filtros con formato {"columna": valor}.
    :return: DataFrame filtrado.
    """
    if df.empty:
        return df

    for col, value in filters.items():
        if col in df.columns:
            if isinstance(value, list) and value:  # Filtrar listas no vacías
                df = df[df[col].isin(value)]
            elif value:  # Filtrar valores individuales
                df = df[df[col] == value]

    return df
