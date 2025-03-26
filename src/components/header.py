# header.py

import dash_bootstrap_components as dbc
from dash import html

def create_header():
    """
    Retorna el componente 'header' con:
      - Logo de OFTW
      - Título de la app
      - Enlaces a GitHub y LinkedIn
    """
    return dbc.Navbar(
        dbc.Container([
            # Logo + Título
            dbc.Row([
                dbc.Col(
                    html.Img(src="https://images.squarespace-cdn.com/content/v1/628957e46790be14e8f78298/fca3bb70-a4cb-4c7f-bddc-7ce6393c61f5/OFTW-Secondary-Logo-RGB-White-4k.png?format=1500w", height="40px"),
                    width="auto"
                ),
                dbc.Col(
                    dbc.NavbarBrand("App Building Challenge", className="ms-2"),
                    width="auto"
                )
            ], align="center", className="g-0"),

            # Enlaces de la derecha
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/TU_GITHUB", external_link=True)),
                    dbc.NavItem(dbc.NavLink("LinkedIn", href="https://linkedin.com/in/TU_LINKEDIN", external_link=True)),
                ],
                navbar=True,
                className="ms-auto"
            )
        ]),
        color="#2675f8ff",      # Un tono acorde a tu palette
        dark=True,            # Texto claro
        className="mb-4"      # Margen inferior para separar del contenido
    )
