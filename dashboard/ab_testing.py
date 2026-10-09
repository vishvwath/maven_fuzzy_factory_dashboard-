from dash import html, dcc
from dash_iconify import DashIconify
import plotly.graph_objects as go

from database import get_data


# ============================================================
# DARK EMERALD THEME COLORS
# ============================================================

THEME_COLORS = {
    "dark_green": "#6EE7B7",
    "green": "#10B981",
    "light_mint": "#34D399",
    "very_light_mint": "#062F2A",
    "white": "#F0FDF4",
    "text": "#D1FAE5",
    "grid": "rgba(110, 231, 183, 0.12)",
    "border": "#075E54",
    "hover_border": "#10B981"
}


# ============================================================
# COMMON DARK CHART THEME
# ============================================================

def apply_chart_theme(fig, title=None, height=450):

    fig.update_layout(
        template="plotly_dark",

        title=dict(
            text=title if title else "",
            font=dict(
                family="Georgia, serif",
                size=22,
                color=THEME_COLORS["text"]
            ),
            x=0.02,
            xanchor="left"
        ),

        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",

        font=dict(
            family="Arial, sans-serif",
            size=14,
            color=THEME_COLORS["text"]
        ),

        xaxis=dict(
            title_font=dict(
                family="Arial, sans-serif",
                size=15,
                color=THEME_COLORS["text"]
            ),

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"],
            linewidth=1
        ),

        yaxis=dict(
            title_font=dict(
                family="Arial, sans-serif",
                size=15,
                color=THEME_COLORS["text"]
            ),

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=True,
            gridcolor=THEME_COLORS["grid"],
            gridwidth=1,
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"],
            linewidth=1
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            bgcolor="rgba(255,255,255,0)"
        ),

        hoverlabel=dict(
            bgcolor="#042722",
            bordercolor=THEME_COLORS["hover_border"],

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color="#F0FDF4"
            )
        ),

        margin=dict(
            l=75,
            r=80,
            t=100,
            b=75
        ),

        height=height
    )

    return fig


# ============================================================
# KPI CARD WITH ICON
# ============================================================

def kpi_card(title, value, icon, icon_class):
    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        title,
                        className="kpi-title",
                        style={"margin": "0 0 8px 0"}
                    ),
                    html.H2(
                        value,
                        className="kpi-value",
                        style={"margin": "0"}
                    )
                ],
                className="kpi-content",
                style={
                    "flex": "1",
                    "minWidth": "0",
                    "paddingRight": "48px"
                }
            ),
            html.Div(
                [
                    DashIconify(
                        icon=icon,
                        width=17,
                        height=17
                    )
                ],
                className=f"kpi-icon {icon_class}",
                style={
                    "position": "absolute",
                    "right": "12px",
                    "top": "12px",
                    "width": "32px",
                    "height": "32px",
                    "minWidth": "32px",
                    "minHeight": "32px",
                    "borderRadius": "50%",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "boxSizing": "border-box"
                }
            )
        ],
        className="kpi-card",
        style={
            "position": "relative",
            "display": "flex",
            "alignItems": "flex-start",
            "minHeight": "88px",
            "padding": "14px 14px 13px 14px",
            "overflow": "hidden"
        }
    )



# ============================================================
# ICONS
# ============================================================

ICON_SESSIONS = "lucide:users"
ICON_ORDERS = "lucide:shopping-cart"
ICON_CONVERSION = "lucide:percent"
ICON_DIFFERENCE = "lucide:trending-up"
ICON_BEST = "lucide:award"


# ============================================================
# A/B TESTING PAGE
# ============================================================

def ab_testing_page():

    # ========================================================
    # 1. LOAD LANDING PAGE A/B TEST DATA
    # ========================================================

    landing_ab_df = get_data(
        """
        SELECT *
        FROM landing_page_ab_test
        """
    )

    # ========================================================
    # 2. LOAD BILLING A/B TEST DATA
    # ========================================================

    billing_ab_df = get_data(
        """
        SELECT *
        FROM billing_ab_test
        """
    )

    # ========================================================
    # PREPARE BILLING VERSION COLUMN
    # ========================================================

    billing_ab_df["billing_version"] = (
        billing_ab_df["billing_version"].astype(str)
    )

    # ========================================================
    # LANDING PAGE A/B TEST VALUES
    # Control = /home
    # Test = /lander-1
    # ========================================================

    control_landing = landing_ab_df[
        landing_ab_df["landing_page"] == "/home"
    ].iloc[0]

    test_landing = landing_ab_df[
        landing_ab_df["landing_page"] == "/lander-1"
    ].iloc[0]

    control_sessions = control_landing["sessions"]
    test_sessions = test_landing["sessions"]

    control_orders = control_landing["orders"]
    test_orders = test_landing["orders"]

    control_conversion = control_landing["conversion_rate"]
    test_conversion = test_landing["conversion_rate"]

    conversion_difference = (
        test_conversion - control_conversion
    )

    better_landing = (
        "Test"
        if test_conversion > control_conversion
        else "Control"
    )

    # ========================================================
    # BILLING A/B TEST VALUES
    # ========================================================

    control_billing = billing_ab_df[
        billing_ab_df["experiment_group"] == "Control"
    ].iloc[0]

    test_billing = billing_ab_df[
        billing_ab_df["experiment_group"] == "Test"
    ].iloc[0]

    control_billing_sessions = control_billing["sessions"]
    test_billing_sessions = test_billing["sessions"]

    control_billing_orders = control_billing["orders"]
    test_billing_orders = test_billing["orders"]

    control_billing_conversion = (
        control_billing["conversion_rate"]
    )

    test_billing_conversion = (
        test_billing["conversion_rate"]
    )

    billing_conversion_difference = (
        test_billing_conversion
        - control_billing_conversion
    )

    better_billing = (
        "Test"
        if test_billing_conversion > control_billing_conversion
        else "Control"
    )

    # ========================================================
    # LANDING PAGE A/B TEST CHART
    # ========================================================

    landing_chart = go.Figure()

    landing_chart.add_trace(
        go.Bar(
            x=landing_ab_df["landing_page"],
            y=landing_ab_df["sessions"],
            name="Sessions",

            text=landing_ab_df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            cliponaxis=False
        )
    )

    landing_chart.add_trace(
        go.Bar(
            x=landing_ab_df["landing_page"],
            y=landing_ab_df["orders"],
            name="Orders",

            text=landing_ab_df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color=THEME_COLORS["green"],
                    width=2
                )
            ),

            cliponaxis=False
        )
    )

    landing_chart.add_trace(
        go.Scatter(
            x=landing_ab_df["landing_page"],
            y=landing_ab_df["conversion_rate"],
            name="Conversion Rate",

            mode="lines+markers+text",

            text=landing_ab_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            line=dict(
                color=THEME_COLORS["text"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["text"],
                size=9,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            yaxis="y2",
            cliponaxis=False
        )
    )

    apply_chart_theme(
        landing_chart,
        title="Landing Page A/B Test",
        height=450
    )

    landing_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Landing Page</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            type="category",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis=dict(
            title=dict(
                text="<b>Sessions / Orders</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            separatethousands=True,

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=True,
            gridcolor=THEME_COLORS["grid"],
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis2=dict(
            title=dict(
                text="<b>Conversion Rate (%)</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            overlaying="y",
            side="right",
            ticksuffix="%",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            )
        )
    )

    # ========================================================
    # LANDING PAGE CONVERSION CHART
    # ========================================================

    landing_conversion_chart = go.Figure()

    landing_conversion_chart.add_trace(
        go.Bar(
            x=landing_ab_df["landing_page"],
            y=landing_ab_df["conversion_rate"],

            text=landing_ab_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color=THEME_COLORS["green"],
                    width=2
                )
            ),

            cliponaxis=False,
            name="Conversion Rate"
        )
    )

    apply_chart_theme(
        landing_conversion_chart,
        title="Landing Page Conversion Rate",
        height=450
    )

    landing_conversion_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Landing Page</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            type="category",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis=dict(
            title=dict(
                text="<b>Conversion Rate (%)</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            ticksuffix="%",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=True,
            gridcolor=THEME_COLORS["grid"],
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        hovermode="x unified"
    )

    # ========================================================
    # BILLING PAGE A/B TEST CHART
    # ========================================================

    billing_chart = go.Figure()

    billing_chart.add_trace(
        go.Bar(
            x=billing_ab_df["billing_version"],
            y=billing_ab_df["sessions"],
            name="Sessions",

            text=billing_ab_df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            cliponaxis=False
        )
    )

    billing_chart.add_trace(
        go.Bar(
            x=billing_ab_df["billing_version"],
            y=billing_ab_df["orders"],
            name="Orders",

            text=billing_ab_df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color=THEME_COLORS["green"],
                    width=2
                )
            ),

            cliponaxis=False
        )
    )

    billing_chart.add_trace(
        go.Scatter(
            x=billing_ab_df["billing_version"],
            y=billing_ab_df["conversion_rate"],
            name="Conversion Rate",

            mode="lines+markers+text",

            text=billing_ab_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            line=dict(
                color=THEME_COLORS["text"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["text"],
                size=9,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            yaxis="y2",
            cliponaxis=False
        )
    )

    apply_chart_theme(
        billing_chart,
        title="Billing Page A/B Test",
        height=450
    )

    billing_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Billing Page</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            type="category",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis=dict(
            title=dict(
                text="<b>Sessions / Orders</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            separatethousands=True,

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=True,
            gridcolor=THEME_COLORS["grid"],
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis2=dict(
            title=dict(
                text="<b>Conversion Rate (%)</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            overlaying="y",
            side="right",
            ticksuffix="%",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            )
        )
    )

    # ========================================================
    # BILLING CONVERSION CHART
    # ========================================================

    billing_conversion_chart = go.Figure()

    billing_conversion_chart.add_trace(
        go.Bar(
            x=billing_ab_df["billing_version"],
            y=billing_ab_df["conversion_rate"],

            text=billing_ab_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="outside",

            textfont=dict(
                family="Arial, sans-serif",
                size=14,
                color=THEME_COLORS["text"]
            ),

            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color=THEME_COLORS["green"],
                    width=2
                )
            ),

            cliponaxis=False,
            name="Conversion Rate"
        )
    )

    apply_chart_theme(
        billing_conversion_chart,
        title="Billing Page Conversion Rate",
        height=450
    )

    billing_conversion_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Billing Page</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            type="category",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        yaxis=dict(
            title=dict(
                text="<b>Conversion Rate (%)</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            ticksuffix="%",

            tickfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            showgrid=True,
            gridcolor=THEME_COLORS["grid"],
            zeroline=False,
            showline=True,
            linecolor=THEME_COLORS["border"]
        ),

        hovermode="x unified"
    )

    # ========================================================
    # PAGE LAYOUT
    # ========================================================

    return html.Div(
        [

            # ==================================================
            # PAGE HEADER
            # ==================================================

            html.Div(
                [
                    html.H1(
                        "A/B Testing",
                        className="page-title"
                    ),

                    html.P(
                        (
                            "Compare control and test experiences "
                            "to evaluate website conversion performance."
                        ),
                        className="page-description"
                    )
                ],
                className="page-header"
            ),

            # ==================================================
            # LANDING PAGE TEST TITLE
            # ==================================================

            html.H2(
                "Landing Page A/B Test",
                className="section-title"
            ),

            html.P(
                (
                    "Compare the /home control page with "
                    "the /lander-1 test page."
                ),
                className="section-description"
            ),

            # ==================================================
            # LANDING PAGE KPI CARDS
            # ==================================================

            html.Div(
                [

                    kpi_card(
                        "Control Sessions",
                        f"{control_sessions:,.0f}",
                        ICON_SESSIONS,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Test Sessions",
                        f"{test_sessions:,.0f}",
                        ICON_SESSIONS,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Control Orders",
                        f"{control_orders:,.0f}",
                        ICON_ORDERS,
                        "aov-icon"
                    ),

                    kpi_card(
                        "Test Orders",
                        f"{test_orders:,.0f}",
                        ICON_ORDERS,
                        "profit-icon"
                    ),

                    kpi_card(
                        "Control Conversion",
                        f"{control_conversion:.2f}%",
                        ICON_CONVERSION,
                        "margin-icon"
                    ),

                    kpi_card(
                        "Test Conversion",
                        f"{test_conversion:.2f}%",
                        ICON_CONVERSION,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Conversion Difference",
                        f"{conversion_difference:+.2f} pp",
                        ICON_DIFFERENCE,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Better Version",
                        better_landing,
                        ICON_BEST,
                        "aov-icon"
                    )

                ],
                className="kpi-container"
            ),

            # ==================================================
            # LANDING PAGE CHARTS
            # ==================================================

            html.Div(
                [

                    html.Div(
                        [
                            dcc.Graph(
                                figure=landing_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-half"
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                figure=landing_conversion_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-half"
                    )

                ],
                className="chart-row"
            ),

            # ==================================================
            # BILLING PAGE TEST TITLE
            # ==================================================

            html.H2(
                "Billing Page A/B Test",
                className="section-title"
            ),

            html.P(
                (
                    "Compare the billing-1 and billing-2 experiences "
                    "using sessions and conversion performance."
                ),
                className="section-description"
            ),

            # ==================================================
            # BILLING KPI CARDS
            # ==================================================

            html.Div(
                [

                    kpi_card(
                        "Control Sessions",
                        f"{control_billing_sessions:,.0f}",
                        ICON_SESSIONS,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Test Sessions",
                        f"{test_billing_sessions:,.0f}",
                        ICON_SESSIONS,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Control Orders",
                        f"{control_billing_orders:,.0f}",
                        ICON_ORDERS,
                        "aov-icon"
                    ),

                    kpi_card(
                        "Test Orders",
                        f"{test_billing_orders:,.0f}",
                        ICON_ORDERS,
                        "profit-icon"
                    ),

                    kpi_card(
                        "Control Conversion",
                        f"{control_billing_conversion:.2f}%",
                        ICON_CONVERSION,
                        "margin-icon"
                    ),

                    kpi_card(
                        "Test Conversion",
                        f"{test_billing_conversion:.2f}%",
                        ICON_CONVERSION,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Conversion Difference",
                        f"{billing_conversion_difference:+.2f} pp",
                        ICON_DIFFERENCE,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Better Version",
                        better_billing,
                        ICON_BEST,
                        "aov-icon"
                    )

                ],
                className="kpi-container"
            ),

            # ==================================================
            # BILLING PAGE CHARTS
            # ==================================================

            html.Div(
                [

                    html.Div(
                        [
                            dcc.Graph(
                                figure=billing_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-half"
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                figure=billing_conversion_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-half"
                    )

                ],
                className="chart-row"
            )

        ],
        className="content",
        style={"backgroundColor": "#031F1C"}
    )