from dash import html, dcc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go

from database import get_data


# ============================================================
# MINT GREEN THEME COLORS
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
    "hover_border": "#10B981",
    "medium_green": "#34D399"
}


# ============================================================
# COMMON CHART THEME
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
# KPI CARD
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
# KPI ICONS
# ============================================================

ICON_SESSIONS = "lucide:users"
ICON_ORDERS = "lucide:shopping-cart"
ICON_CONVERSION = "lucide:percent"
ICON_BOUNCE = "lucide:activity"


# ============================================================
# WEBSITE PAGE
# ============================================================

def website_page():

    # ========================================================
    # 1. WEBSITE KPIs
    # ========================================================

    website_kpi = get_data("""
        SELECT *
        FROM vw_kpi_website
    """)

    kpi = website_kpi.iloc[0]

    landing_sessions = kpi["landing_sessions"]
    completed_orders = kpi["completed_orders"]
    funnel_conversion_rate = kpi["funnel_conversion_rate"]
    bounce_rate = kpi["bounce_rate"]

    # ========================================================
    # 2. MONTHLY WEBSITE TRAFFIC
    # ========================================================

    traffic_df = get_data("""
        SELECT *
        FROM vw_monthly_website_traffic
    """)

    traffic_df = traffic_df.sort_values(
        by=["year", "month"]
    )

    # ========================================================
    # 3. WEBSITE FUNNEL
    # ========================================================

    funnel_df = get_data("""
        SELECT *
        FROM vw_website_funnel
    """)

    # ========================================================
    # 4. LANDING PAGE PERFORMANCE
    # ========================================================

    landing_df = get_data("""
        SELECT *
        FROM landing_page_analysis
    """)

    landing_df = landing_df.sort_values(
        by="revenue",
        ascending=False
    )

    # ========================================================
    # 5. BOUNCE RATE ANALYSIS
    # ========================================================

    bounce_df = get_data("""
        SELECT *
        FROM vw_bounce_rate_analysis
    """)

    # ========================================================
    # MONTHLY WEBSITE TRAFFIC CHART
    # ========================================================

    traffic_chart = go.Figure()

    traffic_chart.add_trace(
        go.Scatter(
            x=traffic_df["year_month"],
            y=traffic_df["sessions"],
            name="Sessions",
            mode="lines+markers",

            line=dict(
                color=THEME_COLORS["text"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["text"],
                size=8,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sessions: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    traffic_chart.add_trace(
        go.Scatter(
            x=traffic_df["year_month"],
            y=traffic_df["users"],
            name="Users",
            mode="lines+markers",

            line=dict(
                color=THEME_COLORS["green"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["green"],
                size=8,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Users: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    traffic_chart.add_trace(
        go.Scatter(
            x=traffic_df["year_month"],
            y=traffic_df["orders"],
            name="Orders",
            mode="lines+markers",

            line=dict(
                color=THEME_COLORS["light_mint"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["medium_green"],
                size=8,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    apply_chart_theme(
        traffic_chart,
        title="Monthly Website Traffic",
        height=450
    )

    traffic_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Month</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

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

        yaxis=dict(
            title=dict(
                text="<b>Count</b>",
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
    # WEBSITE CONVERSION FUNNEL
    # ========================================================

    funnel = funnel_df.iloc[0]

    funnel_labels = [
        "Landing",
        "Products",
        "Product Detail",
        "Cart",
        "Shipping",
        "Billing",
        "Completed Orders"
    ]

    funnel_values = [
        funnel["Landing"],
        funnel["Products"],
        funnel["Product_detail"],
        funnel["Cart"],
        funnel["Shipping"],
        funnel["Billing"],
        funnel["Completed_Orders"]
    ]

    funnel_chart = go.Figure(
        go.Funnel(
            y=funnel_labels,
            x=funnel_values,

            textinfo="value+percent initial",

            # Keep the numbers centered inside the funnel bars
            textposition="inside",
            insidetextanchor="middle",

            # Black text for visibility on all funnel sections
            # Keep the final Completed Orders label unchanged
            textfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=[
                    "#000000",
                    "#000000",
                    "#000000",
                    "#000000",
                    "#000000",
                    "#000000",
                    THEME_COLORS["dark_green"]
                ]
            ),

            marker=dict(
                color=[
                    THEME_COLORS["dark_green"],
                    "#087F5B",
                    THEME_COLORS["green"],
                    "#34D399",
                    THEME_COLORS["light_mint"],
                    "#A7F3D0",
                    THEME_COLORS["very_light_mint"]
                ],

                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Sessions: %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    apply_chart_theme(
        funnel_chart,
        title="Website Conversion Funnel",
        height=450
    )

    funnel_chart.update_layout(
        margin=dict(
            l=100,
            r=70,
            t=100,
            b=45
        )
    )

    # ========================================================
    # LANDING PAGE PERFORMANCE CHART
    # ========================================================

    landing_chart = go.Figure()

    landing_chart.add_trace(
        go.Bar(
            x=landing_df["landing_page"],
            y=landing_df["revenue"],
            name="Revenue",

            text=landing_df["revenue"],
            texttemplate="$%{text:,.0f}",
            textposition="auto",

            textfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["white"]
            ),

            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            yaxis="y",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    landing_chart.add_trace(
        go.Scatter(
            x=landing_df["landing_page"],
            y=landing_df["conversion_rate"],
            name="Conversion Rate",

            mode="lines+markers+text",

            text=landing_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",

            textfont=dict(
                family="Arial, sans-serif",
                size=13,
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

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Conversion Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    apply_chart_theme(
        landing_chart,
        title="Revenue and Conversion Rate by Landing Page",
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
                text="<b>Revenue</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            tickprefix="$",
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
    # BOUNCE RATE ANALYSIS CHART
    # ========================================================

    landing_order = [
        "/home",
        "/lander-1",
        "/lander-2",
        "/lander-3",
        "/lander-4",
        "/lander-5"
    ]

    bounce_df["landing_page"] = pd.Categorical(
        bounce_df["landing_page"],
        categories=landing_order,
        ordered=True
    )

    bounce_df = bounce_df.sort_values(
        by="landing_page"
    )

    bounce_chart = go.Figure()

    # --------------------------------------------------------
    # Sessions
    # --------------------------------------------------------

    bounce_chart.add_trace(
        go.Bar(
            x=bounce_df["landing_page"],
            y=bounce_df["sessions"],

            name="Sessions",

            text=bounce_df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="auto",

            textfont=dict(
                family="Arial, sans-serif",
                size=13,
                color="#000000"
            ),

            marker=dict(
                color=THEME_COLORS["text"],
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sessions: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    # --------------------------------------------------------
    # Bounced Sessions
    # --------------------------------------------------------

    bounce_chart.add_trace(
        go.Bar(
            x=bounce_df["landing_page"],
            y=bounce_df["bounced_sessions"],

            name="Bounced Sessions",

            text=bounce_df["bounced_sessions"],
            texttemplate="%{text:,.0f}",
            textposition="auto",

            textfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["white"]
            ),

            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color=THEME_COLORS["green"],
                    width=2
                )
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Bounced Sessions: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    # --------------------------------------------------------
    # Bounce Rate
    # --------------------------------------------------------

    bounce_chart.add_trace(
        go.Scatter(
            x=bounce_df["landing_page"],
            y=bounce_df["bounce_rate"],

            name="Bounce Rate",

            mode="lines+markers+text",

            text=bounce_df["bounce_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",

            textfont=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            ),

            line=dict(
                color=THEME_COLORS["green"],
                width=3
            ),

            marker=dict(
                color=THEME_COLORS["green"],
                size=9,
                line=dict(
                    color="#042722",
                    width=2
                )
            ),

            yaxis="y2",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Bounce Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    apply_chart_theme(
        bounce_chart,
        title="Bounce Rate Analysis",
        height=450
    )

    bounce_chart.update_layout(
        xaxis=dict(
            title=dict(
                text="<b>Landing Pages</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

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
                text="<b>Sessions</b>",
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
                text="<b>Bounce Rate (%)</b>",
                font=dict(
                    family="Arial, sans-serif",
                    size=15,
                    color=THEME_COLORS["text"]
                )
            ),

            overlaying="y",
            side="right",
            range=[0, 60],
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

        barmode="group",

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
    # ========================================================
    # STAGE CONVERSION ANALYSIS
    # ========================================================

    funnel = funnel_df.iloc[0]

    stage_labels = [
        "Landing → Products",
        "Products → Product Detail",
        "Product Detail → Cart",
        "Cart → Shipping",
        "Shipping → Billing",
        "Billing → Purchase"
    ]

    stage_rates = [
        (funnel["Products"] / funnel["Landing"]) * 100 if funnel["Landing"] else 0,
        (funnel["Product_detail"] / funnel["Products"]) * 100 if funnel["Products"] else 0,
        (funnel["Cart"] / funnel["Product_detail"]) * 100 if funnel["Product_detail"] else 0,
        (funnel["Shipping"] / funnel["Cart"]) * 100 if funnel["Cart"] else 0,
        (funnel["Billing"] / funnel["Shipping"]) * 100 if funnel["Shipping"] else 0,
        (funnel["Completed_Orders"] / funnel["Billing"]) * 100 if funnel["Billing"] else 0
    ]

    stage_conversion_chart = go.Figure()
    stage_conversion_chart.add_trace(go.Bar(
        x=stage_rates,
        y=stage_labels,
        orientation="h",
        name="Conversion Rate",
        text=stage_rates,
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        marker=dict(
            color=THEME_COLORS["green"],
            line=dict(color=THEME_COLORS["dark_green"], width=2)
        ),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Conversion Rate: %{x:.1f}%"
            "<extra></extra>"
        )
    ))

    apply_chart_theme(
        stage_conversion_chart,
        title="Stage Conversion Analysis",
        height=450
    )

    stage_conversion_chart.update_layout(
        xaxis=dict(
            title=dict(text="<b>Conversion Rate (%)</b>"),
            range=[0, max(100, max(stage_rates) + 10)],
            ticksuffix="%",
            showgrid=True,
            gridcolor=THEME_COLORS["grid"]
        ),
        yaxis=dict(
            title=dict(text="<b>Funnel Stage</b>"),
            categoryorder="array",
            categoryarray=stage_labels,
            autorange="reversed"
        ),
        hovermode="closest"
    )

    # PAGE LAYOUT
    # ========================================================

    return html.Div(
        [

            # =================================================
            # HEADER
            # =================================================

            html.Div(
                [
                    html.H1(
                        "Website Analysis",
                        className="page-title"
                    ),

                    html.P(
                        (
                            "Analyze website traffic, conversion funnel, "
                            "landing pages and bounce behavior."
                        ),
                        className="page-description"
                    )
                ],
                className="page-header"
            ),

            # =================================================
            # KPI CARDS
            # =================================================

            html.Div(
                [

                    kpi_card(
                        "Landing Sessions",
                        f"{landing_sessions:,.0f}",
                        ICON_SESSIONS,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Completed Orders",
                        f"{completed_orders:,.0f}",
                        ICON_ORDERS,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Funnel Conversion",
                        f"{funnel_conversion_rate:.2f}%",
                        ICON_CONVERSION,
                        "aov-icon"
                    ),

                    kpi_card(
                        "Bounce Rate",
                        f"{bounce_rate:.2f}%",
                        ICON_BOUNCE,
                        "margin-icon"
                    )

                ],
                className="kpi-container"
            ),

            # =================================================
            # WEBSITE TRAFFIC AND FUNNEL
            # =================================================

            html.H2(
                "Website Traffic & Funnel",
                className="section-title"
            ),

            html.P(
                (
                    "Track monthly website activity and understand "
                    "how sessions move through the conversion funnel."
                ),
                className="section-description"
            ),

            html.Div(
                [

                    html.Div(
                        dcc.Graph(
                            figure=traffic_chart,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        ),
                        className="chart-half"
                    ),

                    html.Div(
                        dcc.Graph(
                            figure=funnel_chart,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        ),
                        className="chart-half"
                    )

                ],
                className="chart-row"
            ),

            # =================================================
            # LANDING PAGE PERFORMANCE
            # =================================================

            html.H2(
                "Landing Page Performance",
                className="section-title"
            ),

            html.P(
                (
                    "Compare landing page revenue, conversion rate "
                    "and bounce behavior."
                ),
                className="section-description"
            ),

            html.Div(
                [

                    html.Div(
                        dcc.Graph(
                            figure=landing_chart,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        ),
                        className="chart-half"
                    ),

                    html.Div(
                        dcc.Graph(
                            figure=bounce_chart,
                            config={
                                "displayModeBar": False,
                                "responsive": True
                            }
                        ),
                        className="chart-half"
                    )

                ],
                className="chart-row"
            ),

            # =================================================
            # STAGE CONVERSION ANALYSIS
            # =================================================
            html.Div(
                dcc.Graph(
                    figure=stage_conversion_chart,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "scrollZoom": True
                    }
                ),
                className="chart-full",
                style={
                    "backgroundColor": "#042722",
                    "border": "1px solid #075E54",
                    "borderRadius": "14px",
                    "padding": "18px 18px 10px",
                    "boxSizing": "border-box",
                    "width": "100%"
                }
            )

        ],
        className="content",
        style={"backgroundColor": "#031F1C"}
    )