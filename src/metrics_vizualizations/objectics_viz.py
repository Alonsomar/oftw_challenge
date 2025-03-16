"""
Genera visualizaciones para Objectives and Key Results (OKRs).
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from log_config import get_logger

logger = get_logger(__name__)

def plot_chapter_arr(df):
    """
    Genera un gráfico de barras para Chapter ARR.

    :param df: DataFrame con el ARR por chapter_type.
    :return: Figura de Plotly.
    """
    if df.empty or "chapter_type" not in df.columns or "ARR_USD" not in df.columns:
        logger.warning("El DataFrame para Chapter ARR está vacío o faltan columnas necesarias.")
        return go.Figure()

    # Rellenar valores NaN y forzar float en ARR_USD
    df["ARR_USD"] = pd.to_numeric(df["ARR_USD"], errors="coerce").fillna(0)

    fig = px.bar(df, x="chapter_type", y="ARR_USD", title="Chapter ARR",
                 labels={"chapter_type": "Chapter Type", "ARR_USD": "Annualized Revenue (USD)"},
                 text_auto=True, color="ARR_USD", color_continuous_scale="blues")

    fig.update_layout(template="plotly_white")

    return fig