import dash_bootstrap_components as dbc
from dash import html

NAV_ITEMS = [
    {
        "id": "money-moved",
        "icon": "fas fa-money-bill-wave",
        "title": "Money Moved",
        "href": "/money_moved",
        "description": "Track financial movements"
    },
    {
        "id": "okrs",
        "icon": "fas fa-bullseye",
        "title": "OKRs",
        "href": "/objectics",
        "description": "Objectives and key results"
    },
    {
        "id": "pledge",
        "icon": "fas fa-handshake",
        "title": "Pledge Performance",
        "href": "/pledge_perf",
        "description": "Analyze pledge metrics"
    }
]

def create_nav_item(item):
    return dbc.NavLink(
        [
            html.Div(
                [
                    html.I(className=f"{item['icon']} nav-icon"),
                    html.Div(
                        [
                            html.Span(item["title"], className="nav-title"),
                            html.Small(item["description"], className="nav-description")
                        ],
                        className="nav-content"
                    )
                ],
                className="nav-item-content"
            )
        ],
        href=item["href"],
        active="exact",
        className="sidebar-nav-link"
    )

sidebar = html.Div(
    [
        # Sin encabezado aquí

        # Navegación principal
        dbc.Nav(
            [create_nav_item(item) for item in NAV_ITEMS],
            vertical=True,
            pills=True,
            className="sidebar-nav"
        ),

        # Footer del sidebar
        html.Div(
            [
                html.Hr(className="sidebar-divider"),
                html.Div(
                    [
                        html.I(className="fas fa-code-branch me-2"),
                        "v1.0.0"
                    ],
                    className="sidebar-footer"
                )
            ],
            className="sidebar-footer-container"
        )
    ],
    id="sidebar",
    className="sidebar"
)
