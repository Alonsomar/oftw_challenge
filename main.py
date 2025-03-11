"""
Punto de entrada para ejecutar la aplicación Dash.
"""

import dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.callbacks.callbacks import register_callbacks

# Inicializar la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurar el layout dinámico
app.layout = create_layout

# Registrar callbacks
register_callbacks(app)

# Ejecutar el servidor
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
