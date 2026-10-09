from dash import html, dcc
import plotly.graph_objects as go
from dash_iconify import DashIconify

from database import get_data


# ============================================================
# DARK EMERALD THEME COLORS
# ============================================================

VI_COLORS = {
    "dark_green": "#6EE7B7",
    "green": "#10B981",
    "light_mint": "#34D399",
    "very_light_mint": "#062F2A",
    "white": "#F0FDF4",
    "text": "#D1FAE5",
    "muted_text": "#94A3B8",
    "grid": "rgba(110, 231, 183, 0.12)",
    "border": "#075E54",
}


VI_CHART_COLORS = [
    VI_COLORS["dark_green"],
    VI_COLORS["green"],
    VI_COLORS["light_mint"],
]


# ============================================================
# APPLY DARK EMERALD CHART THEME
# ============================================================

def apply_vi_chart_theme(fig):
    """Apply the dark emerald theme without changing chart data or logic."""

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",

        font=dict(
            family="Inter, Segoe UI, Arial, sans-serif",
            color=VI_COLORS["text"],
        ),

        title=dict(
            font=dict(
                family="Inter, Segoe UI, Arial, sans-serif",
                size=20,
                color=VI_COLORS["text"],
            )
        ),

        legend=dict(
            font=dict(
                family="Inter, Segoe UI, Arial, sans-serif",
                color=VI_COLORS["text"],
            )
        ),

        hoverlabel=dict(
            bgcolor="#042722",
            bordercolor=VI_COLORS["green"],
            font=dict(
                family="Inter, Segoe UI, Arial, sans-serif",
                color="#F0FDF4",
            ),
        ),

        xaxis=dict(
            color=VI_COLORS["text"],
            linecolor=VI_COLORS["border"],
            gridcolor=VI_COLORS["grid"],
            zerolinecolor=VI_COLORS["border"],
            tickfont=dict(
                color=VI_COLORS["muted_text"]
            ),
            title_font=dict(
                color=VI_COLORS["text"]
            ),
        ),

        yaxis=dict(
            color=VI_COLORS["text"],
            linecolor=VI_COLORS["border"],
            gridcolor=VI_COLORS["grid"],
            zerolinecolor=VI_COLORS["border"],
            tickfont=dict(
                color=VI_COLORS["muted_text"]
            ),
            title_font=dict(
                color=VI_COLORS["text"]
            ),
        ),
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
# CUSTOMER PAGE
# ============================================================

def customer_page():

    # ========================================================
    # 1. NEW VS RETURNING CUSTOMER DATA
    # ========================================================

    new_returning_df = get_data("""
        SELECT *
        FROM new_vs_returning_customers
    """)

    new_returning_df = new_returning_df.sort_values(
        by="revenue",
        ascending=False
    )

    # ========================================================
    # 2. REPEAT CUSTOMER DATA
    # ========================================================

    repeat_kpi = get_data("""
        SELECT *
        FROM vw_kpi_repeat_customer
    """)

    repeat_customers = repeat_kpi.iloc[0]["repeat_customers"]

    # ========================================================
    # 3. REPEAT PURCHASE GAP
    # ========================================================

    purchase_gap_df = get_data("""
        SELECT *
        FROM vw_repeat_purchase_gap
    """)

    # ========================================================
    # CALCULATE CONVERSION RATE
    # ========================================================

    new_returning_df["conversion_rate"] = (
        new_returning_df["orders"]
        / new_returning_df["sessions"]
        * 100
    ).fillna(0)

    # ========================================================
    # CUSTOMER KPIs
    # ========================================================

    total_sessions = new_returning_df["sessions"].sum()
    total_orders = new_returning_df["orders"].sum()
    total_revenue = new_returning_df["revenue"].sum()

    overall_conversion = (
        (total_orders / total_sessions) * 100
        if total_sessions != 0
        else 0
    )

    # ========================================================
    # CHART 1
    # CUSTOMER SESSIONS, ORDERS AND CONVERSION RATE
    # ========================================================

    customer_activity_chart = go.Figure()

    customer_activity_chart.add_trace(
        go.Bar(
            x=new_returning_df["customer_type"],
            y=new_returning_df["sessions"],
            name="Sessions",
            marker_color=VI_COLORS["text"],
            text=new_returning_df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="auto",
            textfont=dict(
                size=15
            ),
            cliponaxis=False
        )
    )

    customer_activity_chart.add_trace(
        go.Bar(
            x=new_returning_df["customer_type"],
            y=new_returning_df["orders"],
            name="Orders",
            marker_color=VI_COLORS["green"],
            text=new_returning_df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="auto",
            textfont=dict(
                size=15
            ),
            cliponaxis=False
        )
    )

    customer_activity_chart.add_trace(
        go.Scatter(
            x=new_returning_df["customer_type"],
            y=new_returning_df["conversion_rate"],
            name="Conversion Rate",
            mode="lines+markers+text",
            text=new_returning_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",
            textfont=dict(
                size=15
            ),
            yaxis="y2",
            line=dict(
                width=3,
                color=VI_COLORS["text"]
            ),
            marker=dict(
                size=9,
                color=VI_COLORS["light_mint"]
            ),
            cliponaxis=False
        )
    )

    customer_activity_chart.update_layout(
        title=dict(
            text="Customer Sessions, Orders & Conversion Rate",
            font=dict(
                size=20
            )
        ),

        xaxis=dict(
            title=dict(
                text="Customer Type",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickfont=dict(
                size=14
            )
        ),

        yaxis=dict(
            title=dict(
                text="Sessions / Orders",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickformat=",",
            tickfont=dict(
                size=14
            )
        ),

        yaxis2=dict(
            title=dict(
                text="Conversion Rate (%)",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            ticksuffix="%",
            overlaying="y",
            side="right",
            tickfont=dict(
                size=14
            )
        ),

        barmode="group",
        template="plotly_dark",
        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(
                size=14
            )
        ),

        margin=dict(
            l=80,
            r=90,
            t=105,
            b=75
        ),

        height=450
    )

    apply_vi_chart_theme(customer_activity_chart)

    # ========================================================
    # CHART 2
    # REVENUE BY CUSTOMER TYPE
    # ========================================================

    customer_revenue_chart = go.Figure()

    customer_revenue_chart.add_trace(
        go.Bar(
            x=new_returning_df["customer_type"],
            y=new_returning_df["revenue"],
            name="Revenue",
            marker_color=VI_COLORS["light_mint"],
            text=new_returning_df["revenue"],
            texttemplate="$%{text:,.0f}",
            textposition="auto",
            textfont=dict(
                size=16
            ),
            cliponaxis=False
        )
    )

    customer_revenue_chart.update_layout(
        title=dict(
            text="Revenue by Customer Type",
            font=dict(
                size=20
            )
        ),

        xaxis=dict(
            title=dict(
                text="Customer Type",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickfont=dict(
                size=14
            )
        ),

        yaxis=dict(
            title=dict(
                text="Revenue ($)",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickprefix="$",
            tickformat=",",
            tickfont=dict(
                size=14
            )
        ),

        template="plotly_dark",
        hovermode="x unified",
        showlegend=False,

        margin=dict(
            l=80,
            r=40,
            t=105,
            b=75
        ),

        height=450
    )

    apply_vi_chart_theme(customer_revenue_chart)

    # ========================================================
    # CHART 3
    # AVERAGE VS MAXIMUM TIME TO SECOND PURCHASE
    # ========================================================

    avg_days = purchase_gap_df.iloc[0][
        "avg_days_to_second_purchase"
    ]

    max_days = purchase_gap_df.iloc[0][
        "max_days"
    ]

    purchase_gap_chart = go.Figure()

    purchase_gap_chart.add_trace(
        go.Bar(
            x=[
                "Average Days",
                "Maximum Days"
            ],

            y=[
                avg_days,
                max_days
            ],

            text=[
                avg_days,
                max_days
            ],

            texttemplate="%{text:.0f} days",
            textposition="auto",

            textfont=dict(
                size=16
            ),

            cliponaxis=False,
            name="Days",
            marker_color=VI_COLORS["green"]
        )
    )

    purchase_gap_chart.update_layout(
        title=dict(
            text="Average vs Maximum Time to Second Purchase",
            font=dict(
                size=20
            )
        ),

        xaxis=dict(
            title=dict(
                text="Purchase Gap",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickfont=dict(
                size=14
            )
        ),

        yaxis=dict(
            title=dict(
                text="Days",
                font=dict(
                    family="Arial Black, Arial, sans-serif",
                    size=16
                )
            ),
            tickformat=",",
            tickfont=dict(
                size=14
            )
        ),

        template="plotly_dark",
        showlegend=False,

        margin=dict(
            l=80,
            r=40,
            t=105,
            b=75
        ),

        height=450
    )

    apply_vi_chart_theme(purchase_gap_chart)

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
                        "Customer Behavior",
                        className="page-title"
                    ),

                    html.P(
                        "Analyze customer activity, revenue and repeat purchase behavior.",
                        className="page-description"
                    )
                ],
                className="page-header"
            ),

            # ==================================================
            # KPI CARDS
            # ==================================================

            html.Div(
                [

                    kpi_card(
                        "Total Customer Sessions",
                        f"{total_sessions:,.0f}",
                        "lucide:users",
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Total Orders",
                        f"{total_orders:,.0f}",
                        "lucide:shopping-cart",
                        "orders-icon"
                    ),

                    kpi_card(
                        "Total Revenue",
                        f"${total_revenue:,.0f}",
                        "lucide:chart-no-axes-column-increasing",
                        "aov-icon"
                    ),

                    kpi_card(
                        "Conversion Rate",
                        f"{overall_conversion:.2f}%",
                        "lucide:percent",
                        "profit-icon"
                    ),

                    kpi_card(
                        "Repeat Customers",
                        f"{repeat_customers:,.0f}",
                        "lucide:user-round-check",
                        "margin-icon"
                    )

                ],
                className="kpi-container"
            ),

            # ==================================================
            # CUSTOMER ACTIVITY
            # ==================================================

            html.H2(
                "Customer Activity",
                className="section-title"
            ),

            html.P(
                "Compare sessions, orders and conversion rate between new and returning customers.",
                className="section-description"
            ),

            html.Div(
                [
                    dcc.Graph(
                        figure=customer_activity_chart,
                        config={
                            "displayModeBar": False
                        }
                    )
                ],
                className="chart-card"
            ),

            # ==================================================
            # CUSTOMER REVENUE AND REPEAT PURCHASE ANALYSIS
            # ==================================================

            html.Div(
                [

                    # ==========================================
                    # CUSTOMER REVENUE
                    # ==========================================

                    html.Div(
                        [

                            html.H2(
                                "Customer Revenue",
                                className="section-title"
                            ),

                            html.P(
                                "Compare revenue generated by new and returning customers.",
                                className="section-description"
                            ),

                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=customer_revenue_chart,
                                        config={
                                            "displayModeBar": False
                                        }
                                    )
                                ],
                                className="chart-card"
                            )

                        ],
                        className="chart-half"
                    ),

                    # ==========================================
                    # REPEAT PURCHASE ANALYSIS
                    # ==========================================

                    html.Div(
                        [

                            html.H2(
                                "Repeat Purchase Analysis",
                                className="section-title"
                            ),

                            html.P(
                                "Compare the average and maximum number of days customers take to make their second purchase.",
                                className="section-description"
                            ),

                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=purchase_gap_chart,
                                        config={
                                            "displayModeBar": False
                                        }
                                    )
                                ],
                                className="chart-card"
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