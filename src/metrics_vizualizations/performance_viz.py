"""
Genera visualizaciones para Pledge Performance Metrics.
"""

import plotly.express as px
import plotly.graph_objects as go
from src.metrics_vizualizations.theme import OFTW_COLOR_SCALES


def plot_breakdown_by_channel(df):
    """
    Genera un gráfico de barras para el breakdown de pledges por canal.

    :param df: DataFrame con breakdown por chapter_type.
    :return: Figura de Plotly.
    """
    if df.empty:
        return go.Figure()

    fig = px.bar(
        df,
        x="chapter_type",
        y="pledge_count",
        labels={"chapter_type": "Chapter Type", "pledge_count": "Pledge Count"},
        text_auto=True,
        color="pledge_count",
        color_continuous_scale=OFTW_COLOR_SCALES['sequential'],
    )

    fig.update_layout(template="oftw_template")

    return fig
