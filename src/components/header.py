import dash_bootstrap_components as dbc
from dash import html

def create_header():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo + texto como una sola unidad alineada
                dbc.NavbarBrand(
                    [
                        html.Img(
                            src="https://images.squarespace-cdn.com/content/v1/628957e46790be14e8f78298/fca3bb70-a4cb-4c7f-bddc-7ce6393c61f5/OFTW-Secondary-Logo-RGB-White-4k.png?format=1500w",
                            height="32px",
                            style={"marginRight": "12px"}
                        ),
                        "App Building Challenge"
                    ],
                    className="d-flex align-items-center navbar-brand-text"
                ),

                # Enlaces
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="fab fa-github me-2"), "GitHub"],
                                href="https://github.com/Alonsomar",
                                external_link=True,
                                className="nav-link-custom"
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="fab fa-linkedin me-2"), "LinkedIn"],
                                href="https://linkedin.com/in/alonso-valdes-gonzalez",
                                external_link=True,
                                className="nav-link-custom"
                            )
                        ),
                    ],
                    className="ms-auto d-flex align-items-center"
                ),
            ],
            fluid=True
        ),
        color="transparent",
        dark=True,
        className="navbar-custom"
    )
