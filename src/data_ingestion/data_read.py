import pandas as pd
import json
from pathlib import Path
from log_config import get_logger
from src.utils.cache import cache

logger = get_logger(__name__)



def load_json_to_dataframe(file_path: Path) -> pd.DataFrame:
    """Carga un archivo JSON en un DataFrame de pandas."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        df = pd.DataFrame(data)
        logger.info(f"Archivo {file_path.name} cargado exitosamente con {df.shape[0]} filas y {df.shape[1]} columnas.")
        return df
    except Exception as e:
        logger.error(f"Error al cargar {file_path.name}: {e}")
        return pd.DataFrame()

@cache.memoize(timeout=300)
def read_data() -> dict:
    """Lee los archivos JSON y devuelve un diccionario con los DataFrames."""
    data_dir = Path(__file__).parent.parent.parent / 'data'
    files = {
        "payments": data_dir / "one-for-the-world-payments.json",
        "pledges": data_dir / "one-for-the-world-pledges.json"
    }

    dataframes = {key: load_json_to_dataframe(path) for key, path in files.items()}
    return dataframes


if __name__ == "__main__":
    dfs = read_data()
    for key, df in dfs.items():
        print(f"{key}: {df.shape}")
