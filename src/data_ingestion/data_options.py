from data_read import read_data
from log_config import get_logger

logger = get_logger(__name__)


def get_unique_values(dataframes: dict) -> dict:
    """Obtiene los valores únicos de cada columna en cada DataFrame."""
    unique_values = {}

    for name, df in dataframes.items():
        if df.empty:
            logger.warning(f"El DataFrame '{name}' está vacío. No se pueden obtener valores únicos.")
            continue

        unique_values[name] = {col: df[col].dropna().unique().tolist() for col in df.columns}
        logger.info(f"Valores únicos extraídos para '{name}'.")

    return unique_values


if __name__ == "__main__":
    dfs = read_data()
    unique_vals = get_unique_values(dfs)

    for dataset, columns in unique_vals.items():
        print(f"\nDataset: {dataset}")
        for col, values in columns.items():
            print(
                f"  {col}: {values[:5]}{'...' if len(values) > 5 else ''}")  # Muestra solo los primeros 5 valores únicos
