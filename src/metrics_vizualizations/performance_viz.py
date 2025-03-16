"""
Genera visualizaciones para Pledge Performance Metrics.
"""

import plotly.express as px
import plotly.graph_objects as go

def plot_breakdown_by_channel(df):
    """
    Genera un gráfico de barras para el breakdown de pledges por canal.

    :param df: DataFrame con breakdown por chapter_type.
    :return: Figura de Plotly.
    """
    if df.empty:
        return go.Figure()

    fig = px.bar(df, x="chapter_type", y="pledge_count", title="Breakdown of Pledges by Channel",
                 labels={"chapter_type": "Chapter Type", "pledge_count": "Pledge Count"},
                 color="pledge_count", color_continuous_scale="blues")
    return fig
