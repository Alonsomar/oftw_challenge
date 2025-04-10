import dash_bootstrap_components as dbc
from dash import html

def create_header():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo + text combined as a single clickable unit, linking to home page
                dbc.NavbarBrand(
                    [
                        html.Img(
                            src="https://images.squarespace-cdn.com/content/v1/628957e46790be14e8f78298/fca3bb70-a4cb-4c7f-bddc-7ce6393c61f5/OFTW-Secondary-Logo-RGB-White-4k.png?format=1500w",
                            height="32px",
                            style={"marginRight": "12px"}
                        ),
                        "App Building Challenge"
                    ],
                    href="/",  # Redirect to home page
                    className="d-flex align-items-center navbar-brand-text"
                ),

                # Navigation items
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [html.I(className="fab fa-github me-2"), "GitHub"],
                                href="https://github.com/Alonsomar/oftw_challenge",
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
