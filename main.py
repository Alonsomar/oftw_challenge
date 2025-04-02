"""
Punto de entrada para ejecutar la aplicación Dash.
"""

import dash
import dash_bootstrap_components as dbc
from src.components.layout import create_layout
from src.callbacks.router_callbacks import register_callbacks
from src.utils.cache import cache
from src.metrics_vizualizations.theme import register_oftw_template

# Inicializar la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# 🔥 Inicializar el cache aquí (después de definir app)
cache.init_app(app.server)

app.title = "OFTW Challenge"

# Registrar theme
register_oftw_template()

# Configurar el layout dinámico
app.layout = create_layout

# Registrar callbacks
register_callbacks(app)

# Ejecutar el servidor
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False, port=8050)
