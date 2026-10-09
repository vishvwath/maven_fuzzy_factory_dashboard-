from dash import html, dcc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go

from database import get_data


# ============================================================
# MINT GREEN / EMERALD GREEN THEME
# ============================================================

THEME_COLORS = {
    "dark_green": "#6EE7B7",
    "green": "#10B981",
    "light_mint": "#34D399",
    "very_light_mint": "#062F2A",
    "medium_green": "#34D399",
    "soft_green": "#047857",
    "white": "#F0FDF4",
    "text": "#D1FAE5",
    "muted_text": "#94A3B8",
    "grid": "rgba(110, 231, 183, 0.12)",
    "border": "#075E54",
    "hover_border": "#10B981",
    "dark_border": "#10B981",
}

CHART_COLORS = [
    "#065F46",
    "#10B981",
    "#34D399",
    "#6EE7B7",
    "#087F5B",
]


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
# KPI ICONS
# ============================================================

ICON_SESSIONS = "lucide:users"
ICON_USERS = "lucide:user-round"
ICON_ORDERS = "lucide:shopping-cart"
ICON_CONVERSION = "lucide:percent"
ICON_REVENUE = "lucide:chart-no-axes-column-increasing"


# ============================================================
# COMMON CHART LAYOUT
# ============================================================

def apply_chart_layout(fig, title):

    fig.update_layout(
        title=dict(
            text=title,
            x=0.05,
            xanchor="left",
            font=dict(
                size=18,
                color=THEME_COLORS["text"]
            )
        ),

        template="plotly_dark",
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",

        height=420,

        margin=dict(
            l=80,
            r=90,
            t=85,
            b=80
        ),

        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                size=14
            )
        ),

        font=dict(
            family="Inter, Segoe UI, Arial, sans-serif",
            size=13,
            color=THEME_COLORS["text"]
        )
    )

    return fig


# ============================================================
# COMBO CHART
# SESSIONS + ORDERS + CONVERSION RATE
# ============================================================

def create_combo_chart(
    df,
    category_column,
    title
):

    fig = go.Figure()


    # ========================================================
    # SESSIONS
    # ========================================================

    fig.add_trace(
        go.Bar(
            x=df[category_column],
            y=df["sessions"],
            name="Sessions",

            # ORIGINAL COLOR
            marker=dict(
                color=THEME_COLORS["green"]
            ),

            text=df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                size=15
            ),

            cliponaxis=False,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sessions: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )


    # ========================================================
    # ORDERS
    # ========================================================

    fig.add_trace(
        go.Bar(
            x=df[category_column],
            y=df["orders"],
            name="Orders",

            # ORIGINAL COLOR
            marker=dict(
                color=THEME_COLORS["text"]
            ),

            text=df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="outside",

            textfont=dict(
                size=15
            ),

            cliponaxis=False,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )


    # ========================================================
    # CONVERSION RATE
    # ========================================================

    fig.add_trace(
        go.Scatter(
            x=df[category_column],
            y=df["conversion_rate"],
            name="Conversion Rate",

            # ORIGINAL MODE
            mode="lines+markers+text",

            text=df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",

            textfont=dict(
                size=15
            ),

            # ORIGINAL COLOR
            line=dict(
                color=THEME_COLORS["soft_green"],
                width=3
            ),

            marker=dict(
                size=8
            ),

            yaxis="y2",
            cliponaxis=False,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Conversion Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )


    # ========================================================
    # COMMON LAYOUT
    # ========================================================

    fig = apply_chart_layout(
        fig,
        title
    )


    # ========================================================
    # AXES
    # ========================================================

    max_conversion = df["conversion_rate"].max()

    fig.update_layout(

        barmode="group",


        # ====================================================
        # X-AXIS
        # ====================================================

        xaxis=dict(

            title=dict(
                text=f"<b>{category_column}</b>",
                font=dict(
                    size=17
                )
            ),

            type="category",
            color=THEME_COLORS["text"],
            gridcolor=THEME_COLORS["grid"],
            linecolor=THEME_COLORS["border"],

            fixedrange=True,

            tickfont=dict(
                size=15
            )
        ),


        # ====================================================
        # PRIMARY Y-AXIS
        # ====================================================

        yaxis=dict(

            title=dict(
                text="<b>Sessions / Orders</b>",
                font=dict(
                    size=17
                )
            ),

            separatethousands=True,
            color=THEME_COLORS["text"],
            gridcolor=THEME_COLORS["grid"],
            linecolor=THEME_COLORS["border"],

            fixedrange=True,

            tickfont=dict(
                size=14
            )
        ),


        # ====================================================
        # SECONDARY Y-AXIS
        # ====================================================

        yaxis2=dict(

            title=dict(
                text="<b>Conversion Rate (%)</b>",
                font=dict(
                    size=17
                )
            ),

            overlaying="y",
            color=THEME_COLORS["text"],
            linecolor=THEME_COLORS["border"],

            side="right",

            range=[
                0,
                max(
                    10,
                    max_conversion * 1.15
                )
            ],

            ticksuffix="%",

            fixedrange=True,

            tickfont=dict(
                size=14
            )
        )
    )

    return fig


# ============================================================
# MARKETING PAGE
# ============================================================

def marketing_page():


    # ========================================================
    # 1. MARKETING KPI
    # Source: vw_kpi_marketing
    # ========================================================

    marketing_kpi = get_data(
        """
        SELECT *
        FROM vw_kpi_marketing
        """
    )

    kpi = marketing_kpi.iloc[0]

    total_sessions = kpi["total_sessions"]
    total_users = kpi["total_users"]
    total_orders = kpi["total_orders"]
    conversion_rate = kpi["conversion_rate"]
    total_revenue = kpi["total_revenue"]


    # ========================================================
    # 2. CAMPAIGN DATA
    # Source: vw_campaign_performance
    # ========================================================

    campaign_df = get_data(
        """
        SELECT *
        FROM vw_campaign_performance
        """
    )


    # ========================================================
    # 3. SEARCH ENGINE COMPARISON
    # ========================================================

    search_engine_df = (
        campaign_df
        .groupby(
            "Search_Engine",
            as_index=False
        )
        .agg(
            sessions=("sessions", "sum"),
            orders=("orders", "sum")
        )
    )

    search_engine_df["conversion_rate"] = (
        search_engine_df["orders"]
        / search_engine_df["sessions"]
        * 100
    )

    total_search_sessions = (
        search_engine_df["sessions"].sum()
    )

    total_search_orders = (
        search_engine_df["orders"].sum()
    )

    total_search_conversion = (
        total_search_orders
        / total_search_sessions
        * 100
    )

    grand_total_search = pd.DataFrame(
        [
            {
                "Search_Engine": "Grand Total",
                "sessions": total_search_sessions,
                "orders": total_search_orders,
                "conversion_rate": total_search_conversion
            }
        ]
    )

    search_engine_chart_df = search_engine_df.copy()


    # ========================================================
    # 4. CAMPAIGN PERFORMANCE
    # ========================================================

    campaign_performance_df = (
        campaign_df
        .groupby(
            "Campaigns",
            as_index=False
        )
        .agg(
            sessions=("sessions", "sum"),
            orders=("orders", "sum")
        )
    )

    campaign_performance_df["conversion_rate"] = (
        campaign_performance_df["orders"]
        / campaign_performance_df["sessions"]
        * 100
    )

    campaign_order = [
        "nonbrand",
        "brand",
        "desktop_targeted",
        "pilot"
    ]

    campaign_performance_df["sort_order"] = (
        campaign_performance_df["Campaigns"]
        .apply(
            lambda x:
            campaign_order.index(x)
            if x in campaign_order
            else 999
        )
    )

    campaign_performance_df = (
        campaign_performance_df
        .sort_values("sort_order")
        .drop(columns="sort_order")
    )


    # ========================================================
    # 5. MARKETING CHANNEL PERFORMANCE
    # ========================================================

    paid_search_brand = campaign_df[
        campaign_df["Campaigns"] == "brand"
    ]

    paid_search_nonbrand = campaign_df[
        campaign_df["Campaigns"] == "nonbrand"
    ]

    socialbook = campaign_df[
        campaign_df["Search_Engine"] == "socialbook"
    ]

    channel_rows = []


    # --------------------------------------------------------
    # Paid Search Brand
    # --------------------------------------------------------

    brand_sessions = paid_search_brand["sessions"].sum()
    brand_orders = paid_search_brand["orders"].sum()

    channel_rows.append(
        {
            "channel_group": "Paid Search Brand",
            "sessions": brand_sessions,
            "orders": brand_orders
        }
    )


    # --------------------------------------------------------
    # Paid Search Non-Brand
    # --------------------------------------------------------

    nonbrand_sessions = (
        paid_search_nonbrand["sessions"].sum()
    )

    nonbrand_orders = (
        paid_search_nonbrand["orders"].sum()
    )

    channel_rows.append(
        {
            "channel_group": "Paid Search Non-Brand",
            "sessions": nonbrand_sessions,
            "orders": nonbrand_orders
        }
    )


    # --------------------------------------------------------
    # Socialbook
    # --------------------------------------------------------

    social_sessions = socialbook["sessions"].sum()
    social_orders = socialbook["orders"].sum()

    channel_rows.append(
        {
            "channel_group": "socialbook",
            "sessions": social_sessions,
            "orders": social_orders
        }
    )

    channel_df = pd.DataFrame(channel_rows)

    channel_df["conversion_rate"] = (
        channel_df["orders"]
        / channel_df["sessions"]
        * 100
    )


    # ========================================================
    # 6. DEVICE PERFORMANCE
    # Source: vw_device_performance
    # ========================================================

    device_df = get_data(
        """
        SELECT *
        FROM vw_device_performance
        """
    )


    # ========================================================
    # 7. CREATE CHARTS
    # ========================================================

    # --------------------------------------------------------
    # Marketing Channel Performance
    # --------------------------------------------------------

    channel_chart = create_combo_chart(
        channel_df,
        "channel_group",
        "Marketing Channel Performance"
    )


    # --------------------------------------------------------
    # Search Engine Comparison
    # --------------------------------------------------------

    search_engine_chart = create_combo_chart(
        search_engine_chart_df,
        "Search_Engine",
        "Search Engine Comparison"
    )


    # --------------------------------------------------------
    # Campaign Performance
    # --------------------------------------------------------

    campaign_chart = create_combo_chart(
        campaign_performance_df,
        "Campaigns",
        "Campaign Performance"
    )


    # --------------------------------------------------------
    # Device Performance
    # --------------------------------------------------------

    device_chart = create_combo_chart(
        device_df,
        "device_type",
        "Device Performance"
    )


    # ========================================================
    # 8. PAGE LAYOUT
    # ========================================================

    return html.Div(
        [


            # =================================================
            # PAGE HEADER
            # =================================================

            html.Div(
                [
                    html.H1(
                        "Marketing Analytics",
                        className="page-title"
                    ),

                    html.P(
                        (
                            "Compare traffic, orders and conversion "
                            "performance across marketing channels, "
                            "search engines, campaigns and devices."
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
                        "Total Sessions",
                        f"{total_sessions:,.0f}",
                        ICON_SESSIONS,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Total Users",
                        f"{total_users:,.0f}",
                        ICON_USERS,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Total Orders",
                        f"{total_orders:,.0f}",
                        ICON_ORDERS,
                        "aov-icon"
                    ),

                    kpi_card(
                        "Conversion Rate",
                        f"{conversion_rate:.2f}%",
                        ICON_CONVERSION,
                        "profit-icon"
                    ),

                    kpi_card(
                        "Total Revenue",
                        f"${total_revenue:,.0f}",
                        ICON_REVENUE,
                        "margin-icon"
                    )

                ],

                className="kpi-container"
            ),


            # =================================================
            # TOP ROW
            # MARKETING CHANNEL + SEARCH ENGINE
            # =================================================

            html.Div(
                [


                    # -----------------------------------------
                    # Marketing Channel Performance
                    # -----------------------------------------

                    html.Div(
                        [

                            dcc.Graph(
                                figure=channel_chart,

                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                },

                                style={
                                    "width": "100%"
                                }
                            )

                        ],

                        className="chart-half"
                    ),


                    # -----------------------------------------
                    # Search Engine Comparison
                    # -----------------------------------------

                    html.Div(
                        [

                            dcc.Graph(
                                figure=search_engine_chart,

                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                },

                                style={
                                    "width": "100%"
                                }
                            )

                        ],

                        className="chart-half"
                    )

                ],

                className="chart-row"
            ),


            # =================================================
            # BOTTOM ROW
            # CAMPAIGN + DEVICE PERFORMANCE
            # =================================================

            html.Div(
                [


                    # -----------------------------------------
                    # Campaign Performance
                    # -----------------------------------------

                    html.Div(
                        [

                            dcc.Graph(
                                figure=campaign_chart,

                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                },

                                style={
                                    "width": "100%"
                                }
                            )

                        ],

                        className="chart-half"
                    ),


                    # -----------------------------------------
                    # Device Performance
                    # -----------------------------------------

                    html.Div(
                        [

                            dcc.Graph(
                                figure=device_chart,

                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                },

                                style={
                                    "width": "100%"
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