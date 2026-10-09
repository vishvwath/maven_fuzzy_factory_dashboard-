from dash import Dash, html, dcc, Input, Output, ctx

from revenue import revenue_page
from marketing import marketing_page
from website import website_page
from product import product_page
from customer import customer_page
from ab_testing import ab_testing_page


# ============================================================
# CREATE DASH APPLICATION
# ============================================================

app = Dash(
    __name__,
    title="Maven Fuzzy Factory Analytics",
    suppress_callback_exceptions=True
)

server = app.server


# ============================================================
# DASHBOARD OPTIONS
# ============================================================

dashboard_options = [
    {"label": "Revenue & Sales", "value": "revenue"},
    {"label": "Marketing", "value": "marketing"},
    {"label": "Website Performance", "value": "website"},
    {"label": "Customer Analysis", "value": "customer"},
    {"label": "Product Analysis", "value": "product"},
    {"label": "A/B Testing", "value": "ab_testing"},
]


# ============================================================
# SIDEBAR NAVIGATION ITEM
# ============================================================

def nav_item(label, value, icon):
    return html.Button(
        [
            html.Span(icon, className="nav-icon"),
            html.Span(label, className="nav-label"),
        ],
        id=f"nav-{value}",
        n_clicks=0,
        className="sidebar-nav-item",
        title=label
    )


# ============================================================
# DESKTOP SIDEBAR
# ============================================================

sidebar = html.Aside(
    [
        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    "M",
                    className="brand-mark"
                ),

                html.Div(
                    [
                        html.H2(
                            "Maven Fuzzy",
                            className="sidebar-brand-title"
                        ),

                        html.P(
                            "Factory Analytics",
                            className="sidebar-brand-subtitle"
                        )
                    ],
                    className="sidebar-brand-text"
                )
            ],
            className="sidebar-brand"
        ),

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            "⌕",
                            className="search-icon"
                        ),

                        dcc.Input(
                            id="sidebar-search",
                            type="text",
                            placeholder="Search dashboard",
                            className="sidebar-search-input"
                        )
                    ],
                    className="sidebar-search"
                )
            ],
            className="sidebar-search-wrapper"
        ),

        # ----------------------------------------------------
        # DIVIDER
        # ----------------------------------------------------

        html.Div(
            className="sidebar-divider"
        ),

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        html.P(
            "NAVIGATION",
            className="sidebar-section-label"
        ),

        html.Nav(
            [
                nav_item("Revenue", "revenue", "◈"),
                nav_item("Marketing", "marketing", "↗"),
                nav_item("Website", "website", "⌁"),
                nav_item("Customer", "customer", "◉"),
                nav_item("Product", "product", "◇"),
                nav_item("A/B Testing", "ab_testing", "A/B"),
            ],
            className="sidebar-nav"
        ),

        # ----------------------------------------------------
        # SPACER
        # ----------------------------------------------------

        html.Div(
            className="sidebar-spacer"
        ),

        # ----------------------------------------------------
        # SETTINGS
        # ----------------------------------------------------

        html.Button(
            [
                html.Span("⚙", className="nav-icon"),
                html.Span("Settings", className="nav-label"),
            ],
            id="settings-button",
            n_clicks=0,
            className="sidebar-nav-item sidebar-settings"
        ),

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        html.Div(
            [
                html.Div(
                    className="status-dot"
                ),

                html.Div(
                    [
                        html.P(
                            "DATA ANALYTICS",
                            className="sidebar-status-title"
                        ),

                        html.P(
                            "SQL • Python • Dash • Plotly",
                            className="sidebar-status-text"
                        )
                    ]
                )
            ],
            className="sidebar-status"
        ),

        html.P(
            "Maven Fuzzy Factory",
            className="sidebar-footer"
        )
    ],
    className="sidebar"
)


# ============================================================
# MOBILE HEADER
# ============================================================

mobile_header = html.Div(
    [
        html.Div(
            [
                html.Div(
                    "M",
                    className="mobile-brand-mark"
                ),

                html.Div(
                    [
                        html.H2(
                            "Maven Fuzzy",
                            className="mobile-brand-title"
                        ),

                        html.P(
                            "Factory Analytics",
                            className="mobile-brand-subtitle"
                        )
                    ],
                    className="mobile-brand-text"
                )
            ],
            className="mobile-brand"
        ),

        dcc.Dropdown(
            id="mobile-page-selector",
            options=dashboard_options,
            value="revenue",
            clearable=False,
            searchable=False,
            className="mobile-dashboard-dropdown"
        )
    ],
    className="mobile-header"
)


# ============================================================
# MAIN CONTENT
# ============================================================

content = html.Main(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "MAVEN FUZZY FACTORY",
                            className="content-eyebrow"
                        ),

                        html.P(
                            "E-COMMERCE ANALYTICS",
                            className="content-context"
                        )
                    ],
                    className="content-context-group"
                ),

                html.Div(
                    [
                        html.Div(
                            className="live-indicator"
                        ),

                        html.Span(
                            "Analytics workspace",
                            className="live-text"
                        )
                    ],
                    className="workspace-status"
                )
            ],
            className="content-topbar"
        ),

        html.Div(
            id="page-content",
            className="content"
        )
    ],
    className="main-area"
)


# ============================================================
# APPLICATION LAYOUT
# ============================================================

app.layout = html.Div(
    [
        sidebar,
        mobile_header,
        content
    ],
    className="app-shell"
)


# ============================================================
# PLACEHOLDER PAGE
# ============================================================

def placeholder_page(title, description):

    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        "EXECUTIVE DASHBOARD",
                        className="page-eyebrow"
                    ),

                    html.H1(
                        title,
                        className="page-title"
                    ),

                    html.P(
                        description,
                        className="page-description"
                    )
                ],
                className="page-header"
            ),

            html.Div(
                [
                    html.Div(
                        "01",
                        className="placeholder-number"
                    ),

                    html.Div(
                        [
                            html.H3(
                                "Dashboard Section",
                                className="section-title"
                            ),

                            html.P(
                                "This section will use the existing SQL "
                                "views and display the results using Plotly.",
                                className="section-description"
                            )
                        ],
                        className="placeholder-copy"
                    )
                ],
                className="placeholder-header"
            )
        ],
        className="placeholder-card"
    )


# ============================================================
# PAGE NAVIGATION
# ============================================================

@app.callback(
    Output(
        "page-content",
        "children"
    ),

    [
        Input("nav-revenue", "n_clicks"),
        Input("nav-marketing", "n_clicks"),
        Input("nav-website", "n_clicks"),
        Input("nav-customer", "n_clicks"),
        Input("nav-product", "n_clicks"),
        Input("nav-ab_testing", "n_clicks"),
        Input("mobile-page-selector", "value"),
    ]
)
def display_page(
    revenue_clicks,
    marketing_clicks,
    website_clicks,
    customer_clicks,
    product_clicks,
    ab_testing_clicks,
    mobile_page
):

    triggered = ctx.triggered_id

    # --------------------------------------------------------
    # MOBILE DROPDOWN
    # --------------------------------------------------------

    if triggered == "mobile-page-selector":
        page = mobile_page

    # --------------------------------------------------------
    # DESKTOP SIDEBAR
    # --------------------------------------------------------

    elif triggered == "nav-revenue":
        page = "revenue"

    elif triggered == "nav-marketing":
        page = "marketing"

    elif triggered == "nav-website":
        page = "website"

    elif triggered == "nav-customer":
        page = "customer"

    elif triggered == "nav-product":
        page = "product"

    elif triggered == "nav-ab_testing":
        page = "ab_testing"

    # --------------------------------------------------------
    # DEFAULT PAGE
    # --------------------------------------------------------

    else:
        page = "revenue"

    # --------------------------------------------------------
    # PAGE CONTENT
    # --------------------------------------------------------

    if page == "revenue":
        return revenue_page()

    elif page == "marketing":
        return marketing_page()

    elif page == "website":
        return website_page()

    elif page == "customer":
        return customer_page()

    elif page == "product":
        return product_page()

    elif page == "ab_testing":
        return ab_testing_page()

    return revenue_page()


# ============================================================
# MOBILE / DESKTOP NAVIGATION SYNC
# ============================================================

@app.callback(
    [
        Output("mobile-page-selector", "value"),
        Output("nav-revenue", "className"),
        Output("nav-marketing", "className"),
        Output("nav-website", "className"),
        Output("nav-customer", "className"),
        Output("nav-product", "className"),
        Output("nav-ab_testing", "className"),
    ],
    [
        Input("nav-revenue", "n_clicks"),
        Input("nav-marketing", "n_clicks"),
        Input("nav-website", "n_clicks"),
        Input("nav-customer", "n_clicks"),
        Input("nav-product", "n_clicks"),
        Input("nav-ab_testing", "n_clicks"),
        Input("mobile-page-selector", "value"),
    ]
)
def sync_navigation(
    revenue_clicks,
    marketing_clicks,
    website_clicks,
    customer_clicks,
    product_clicks,
    ab_testing_clicks,
    mobile_page
):

    triggered = ctx.triggered_id

    if triggered == "nav-revenue":
        page = "revenue"

    elif triggered == "nav-marketing":
        page = "marketing"

    elif triggered == "nav-website":
        page = "website"

    elif triggered == "nav-customer":
        page = "customer"

    elif triggered == "nav-product":
        page = "product"

    elif triggered == "nav-ab_testing":
        page = "ab_testing"

    elif triggered == "mobile-page-selector":
        page = mobile_page

    else:
        page = "revenue"

    def nav_class(value):
        if value == page:
            return "sidebar-nav-item active"
        return "sidebar-nav-item"

    return (
        page,
        nav_class("revenue"),
        nav_class("marketing"),
        nav_class("website"),
        nav_class("customer"),
        nav_class("product"),
        nav_class("ab_testing"),
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)