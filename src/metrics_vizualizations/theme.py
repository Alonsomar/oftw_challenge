# src/metrics_vizualizations/theme.py

import plotly.graph_objects as go
import plotly.io as pio

# 1) Paleta de colores corporativos (variables CSS, replicadas aquí en Hex)
OFTW_COLORS = {
    "blue_crayola": "#2675f8",
    "giants_orange": "#fb6a37",
    "chartreuse": "#e2ff3f",
    "plum_web": "#e8ace7",
    "mexican_pink": "#dc0073",
}

# 2) Define escalas continuas divergentes / secuenciales
#    (Si quieres personalizar 'sequentialminus', hazlo igual que 'sequential')
OFTW_COLOR_SCALES = {
    'diverging': [
        [0.0, '#dc0073'],  # extremo rosado
        [0.5, '#ffffff'],  # punto neutro (blanco)
        [1.0, '#2675f8']  # extremo azul
    ],
    'sequential': [
        [0.0, '#fde4ef'],
        [0.5, '#dc0073'],
        [1.0, '#a30055']
    ],
    'sequentialminus': [
        [0.0, '#a30055'],
        [0.5, '#dc0073'],
        [1.0, '#fde4ef']
    ],
    'discrete': [
        "#2675f8",
        "#fb6a37",
        "#e2ff3f",
        "#e8ace7",
        "#dc0073"
    ]
}


def register_oftw_template():
    """
    Registra un template de Plotly con estilos profesionales y
    alineados a la identidad de la app.
    """

    # 3) Ajustes globales de layout
    oftw_layout = go.Layout(
        # 3.a) Fuentes y colores de texto
        font=dict(
            family="Montserrat, sans-serif",  # misma que en tu CSS
            size=14,
            color="#212121"  # var(--text-primary)
        ),
        # 3.b) Título centrado
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=18)  # puedes aumentar más si lo deseas
        ),
        # 3.c) Márgenes y colores de fondo
        margin=dict(t=50, b=40, l=50, r=50),
        paper_bgcolor="white",
        plot_bgcolor="white",

        # 3.d) Leyenda horizontal arriba
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        # 3.e) Ejes con grid sutil
        xaxis=dict(
            showgrid=True,
            gridcolor="#e0e0e0",  # var(--border-color)
            linecolor="#e0e0e0",
            ticks="outside",
            tickcolor="rgba(0,0,0,0)",
            automargin=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#e0e0e0",
            linecolor="#e0e0e0",
            ticks="outside",
            tickcolor="rgba(0,0,0,0)",
            automargin=True
        ),

        # 3.f) colorway para series categóricas
        colorway=[
            OFTW_COLORS["mexican_pink"],
            OFTW_COLORS["chartreuse"],
            OFTW_COLORS["blue_crayola"],
            OFTW_COLORS["giants_orange"],
            OFTW_COLORS["plum_web"],
        ],

        # 3.g) coloraxis para variables continuas (cuando usas coloraxis)
        coloraxis=dict(
            colorscale=OFTW_COLOR_SCALES['sequential']  # por defecto, scale secuencial
        ),

        # Opcionales: annotationdefaults, shapedefaults, etc.
        annotationdefaults=dict(
            arrowcolor="#212121",
            arrowhead=0
        ),
        shapedefaults=dict(
            line=dict(color="#212121")
        )
    )

    # 4) Definir data defaults para ciertos tipos de traza (opcional)
    #    De esta forma, si creas un Heatmap y NO especificas colorscale,
    #    usará la escala que definas aquí automáticamente.
    data_defaults = {
        "heatmap": [go.Heatmap(colorscale=OFTW_COLOR_SCALES['sequential'])],
        "choropleth": [go.Choropleth(colorscale=OFTW_COLOR_SCALES['diverging'])],
        "surface": [go.Surface(colorscale=OFTW_COLOR_SCALES['sequentialminus'])]
        # agrega más si usas other trace types como 'scatter3d', 'histogram2d', etc.
    }

    oftw_template = go.layout.Template(
        layout=oftw_layout,
        data=data_defaults
    )

    # 5) Registrar con un nombre (oftw_template)
    pio.templates["oftw_template"] = oftw_template


def apply_oftw_template(fig):
    """
    Aplica el tema "oftw_template" a la figura dada.
    """
    fig.update_layout(template="oftw_template")
    return fig
