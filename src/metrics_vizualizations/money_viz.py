"""
Genera visualizaciones interactivas para 'Money Moved' y 'Counterfactual Money Moved'.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from log_config import get_logger
from src.metrics_calculations.money_metrics import calculate_money_moved, calculate_counterfactual_money_moved
from src.metrics_vizualizations.theme import OFTW_COLOR_SCALES

logger = get_logger(__name__)

def plot_money_moved(monthly_money_moved: pd.DataFrame, total_money_moved: float) -> go.Figure:
    """
    Genera un gráfico de Money Moved a lo largo del tiempo.

    :param monthly_money_moved: DataFrame con Money Moved agregado por mes.
    :param total_money_moved: Valor total de Money Moved.
    :return: Figura de Plotly.
    """
    if monthly_money_moved.empty:
        logger.warning("El DataFrame de Money Moved está vacío. No se generará gráfico.")
        return go.Figure()

    fig = px.line(
        monthly_money_moved,
        x="year_month",
        y="amount_usd",
        labels={"year_month": "Month", "amount_usd": "Money Moved (USD)"},
        markers=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Money Moved (USD)",
        template="oftw_template"
    )

    return fig

def plot_counterfactual_money_moved(monthly_counterfactual_money_moved: pd.DataFrame, total_counterfactual_money_moved: float) -> go.Figure:
    """
    Genera un gráfico de Counterfactual Money Moved a lo largo del tiempo.

    :param monthly_counterfactual_money_moved: DataFrame con Money Moved contrafactual agregado por mes.
    :param total_counterfactual_money_moved: Valor total de Money Moved contrafactual.
    :return: Figura de Plotly.
    """
    if monthly_counterfactual_money_moved.empty:
        logger.warning("El DataFrame de Money Moved contrafactual está vacío. No se generará gráfico.")
        return go.Figure()

    fig = px.bar(
        monthly_counterfactual_money_moved,
        x="year_month",
        y="counterfactual_amount",
        labels={"year_month": "Month", "counterfactual_amount": "Counterfactual Money Moved (USD)"},
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Counterfactual Money Moved (USD)",
        template="oftw_template"
    )

    return fig


def plot_money_moved_by_platform(df):
    """
    Genera un gráfico de barras para Money Moved por plataforma de pago.

    :param df: DataFrame con Money Moved por plataforma.
    :return: Figura de Plotly.
    """
    if df.empty or "payment_platform" not in df.columns or "amount_usd" not in df.columns:
        logger.warning("El DataFrame para Money Moved por plataforma está vacío o faltan columnas necesarias.")
        return go.Figure()

    # Rellenar valores NaN y convertir a float
    df["amount_usd"] = pd.to_numeric(df["amount_usd"], errors="coerce").fillna(0)

    fig = px.bar(
        df,
        x="payment_platform",
        y="amount_usd",
        labels={"payment_platform": "Payment Platform", "amount_usd": "Money Moved (USD)"},
        text_auto=True,
        color="amount_usd",
        color_continuous_scale=OFTW_COLOR_SCALES['sequential'],
    )

    fig.update_layout(template="oftw_template")

    return fig


def plot_money_moved_by_donation_type(df: pd.DataFrame) -> go.Figure:
    """
    Genera un gráfico de pastel para Money Moved por tipo de donación (One-Time vs Recurring).

    :param df: DataFrame con Money Moved por tipo de donación.
    :return: Figura de Plotly.
    """
    if df.empty:
        logger.warning("El DataFrame de Money Moved por tipo de donación está vacío. No se generará gráfico.")
        return go.Figure()

    fig = px.pie(
        df,
        names="donation_type",
        values="amount_usd",
        hole=0.4,
        labels={"donation_type": "Donation Type", "amount_usd": "Money Moved (USD)"}
    )

    fig.update_layout(template="oftw_template")
    return fig


def plot_money_moved_treemap(df: pd.DataFrame) -> go.Figure:
    """
    Genera un Treemap para visualizar Money Moved por fuente.

    :param df: DataFrame con Money Moved por fuente.
    :return: Figura de Plotly.
    """
    if df.empty:
        logger.warning("El DataFrame de Money Moved por fuente está vacío. No se generará gráfico.")
        return go.Figure()

    fig = px.treemap(
        df,
        path=["chapter_type", "donor_chapter"],
        values="amount_usd",
        color="amount_usd",
        color_continuous_scale=OFTW_COLOR_SCALES['sequential'],
    )

    fig.update_layout(template="oftw_template")

    return fig


def plot_accumulated_money_moved(accumulated_df: pd.DataFrame,
                                 target_value: float = None,
                                 year_mode: str = "calendar") -> go.Figure:
    """
    Grafica el 'cumulative_usd' para cada contable_year en lines.
    """
    if accumulated_df.empty:
        return go.Figure()

    # Ejemplo: multiples lines, color por contable_year
    fig = px.line(
        accumulated_df,
        x="contable_month",  # o "year_month_label"
        y="cumulative_usd",
        color="contable_year",
        color_discrete_sequence=OFTW_COLOR_SCALES['discrete'],
        markers=True,
        labels={
            "contable_month": "Month in Year",
            "cumulative_usd": "Cumulative USD",
            "contable_year": "Year"
        }
    )

    # Agregar meta
    if target_value:
        fig.add_hline(
            y=target_value,
            line_dash="dot",
            line_color="red",
            annotation_text=f"Target: ${target_value:,.0f}",
            annotation_position="top left"
        )

        # 2) Añadir la línea vertical que marca diciembre,
        #    según sea calendar o fiscal
        if year_mode == "calendar":
            # x=12 => Diciembre
            fig.add_vline(
                x=12,
                line_dash="dash",
                line_width=1,
                line_color="green",
                annotation_text="December",
                annotation_position="top right"
            )
        else:
            # year_mode == "fiscal"
            # x=6 => Diciembre en contable_month con offset
            fig.add_vline(
                x=6,
                line_dash="dash",
                line_color="green",
                annotation_text="December",
                annotation_position="top right"
            )

    fig.update_layout(template="oftw_template")
    return fig


if __name__ == "__main__":
    from src.data_ingestion.data_read import read_data
    from src.data_ingestion.data_transform import clean_data

    # Cargar y transformar datos
    dfs = read_data()
    transformed_dfs = clean_data(dfs)

    # Obtener pagos
    payments_df = transformed_dfs.get("payments", pd.DataFrame())

    # Calcular métricas
    monthly_money_moved, total_money_moved = calculate_money_moved(payments_df)
    monthly_counterfactual_money_moved, total_counterfactual_money_moved = calculate_counterfactual_money_moved(payments_df)

    # Generar gráficos
    fig1 = plot_money_moved(monthly_money_moved, total_money_moved)
    fig2 = plot_counterfactual_money_moved(monthly_counterfactual_money_moved, total_counterfactual_money_moved)

    # Mostrar gráficos
    fig1.show()
    fig2.show()


