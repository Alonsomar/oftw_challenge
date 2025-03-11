"""
Carga los datos desde los JSON y aplica transformaciones iniciales.
"""

from src.data_ingestion.data_read import read_data
from src.data_ingestion.data_transform import clean_data

def load_clean_data():
    """
    Carga y transforma los datos de pagos y pledges.

    :return: Diccionario con DataFrames de datos limpios.
    """
    dfs = read_data()
    return clean_data(dfs)
