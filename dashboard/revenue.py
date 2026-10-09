from dash import html, dcc
import plotly.express as px
from dash_iconify import DashIconify
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
    "muted_text": "#94A3B8",
    "grid": "rgba(110, 231, 183, 0.12)",
    "border": "#075E54",
    "hover_border": "#10B981",
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
            color=THEME_COLORS["muted_text"]
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
                color=THEME_COLORS["muted_text"]
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
                color=THEME_COLORS["muted_text"]
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

            bgcolor="rgba(0,0,0,0)"
        ),

        hoverlabel=dict(
            bgcolor="#042722",
            bordercolor=THEME_COLORS["hover_border"],

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            )
        ),

        margin=dict(
            l=75,
            r=45,
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
# BOLD AXIS TITLE HELPER
# ============================================================

def bold_axis_title(text):

    return dict(
        text=f"<b>{text}</b>",
        font=dict(
            family="Arial, sans-serif",
            size=15,
            color=THEME_COLORS["text"]
        )
    )


# ============================================================
# YEARLY REVENUE
# SQL VIEW: vw_yearly_revenue
# ============================================================

def yearly_revenue():

    query = """
        SELECT *
        FROM vw_yearly_revenue
        ORDER BY Year
    """

    df = get_data(query)

    fig = px.pie(
        df,
        names="Year",
        values="Yearly_revenue",
        title="Yearly Revenue",
        hole=0.45,

        color_discrete_sequence=[
            THEME_COLORS["dark_green"],
            THEME_COLORS["green"],
            THEME_COLORS["light_mint"],
            "#34D399",
            THEME_COLORS["very_light_mint"]
        ]
    )

    fig.update_traces(
        texttemplate="$%{value:,.0f}<br>(%{percent})",
        textposition="inside",

        textfont=dict(
            family="Arial, sans-serif",
            size=13,
            color=THEME_COLORS["text"]
        ),

        hovertemplate=(
            "<b>%{label}</b><br>"
            "Revenue: $%{value:,.0f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),

        marker=dict(
            line=dict(
                color="#042722",
                width=2
            )
        )
    )

    apply_chart_theme(
        fig,
        title="Yearly Revenue",
        height=450
    )

    fig.update_layout(
        showlegend=True,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,

            font=dict(
                family="Arial, sans-serif",
                size=13,
                color=THEME_COLORS["text"]
            )
        ),

        margin=dict(
            l=30,
            r=30,
            t=90,
            b=70
        )
    )

    return dcc.Graph(
        figure=fig,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# MONTH-OVER-MONTH REVENUE GROWTH
# SQL VIEW: vw_mom_revenue_growth
# ============================================================

def mom_revenue_growth():

    query = """
        SELECT *
        FROM vw_mom_revenue_growth
        ORDER BY month
    """

    df = get_data(query)

    fig = px.line(
        df,
        x="month",
        y="growth_percentage",
        markers=True,
        title="Month-over-Month Revenue Growth"
    )

    fig.update_traces(
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

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue Growth: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=THEME_COLORS["text"],
        line_width=2
    )

    apply_chart_theme(
        fig,
        title="Month-over-Month Revenue Growth",
        height=450
    )

    fig.update_layout(
        xaxis=dict(
            title=bold_axis_title("Month")
        ),

        yaxis=dict(
            title=bold_axis_title("Revenue Growth (%)"),
            ticksuffix="%"
        ),

        hovermode="x unified",

        margin=dict(
            l=75,
            r=45,
            t=100,
            b=75
        )
    )

    return dcc.Graph(
        figure=fig,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# MONTHLY REVENUE AND PROFIT
# SQL VIEW: vw_monthly_revenue_profit
# ============================================================

def monthly_revenue_profit():

    query = """
        SELECT *
        FROM vw_monthly_revenue_profit
        ORDER BY year, month_number
    """

    df = get_data(query)

    df["period"] = (
        df["year"].astype(str)
        + " "
        + df["month"]
    )

    chart_data = df.melt(
        id_vars=["period"],

        value_vars=[
            "revenue",
            "profit"
        ],

        var_name="Metric",
        value_name="Amount"
    )

    fig = px.line(
        chart_data,
        x="period",
        y="Amount",
        color="Metric",
        markers=True,
        title="Monthly Revenue & Profit",

        color_discrete_map={
            "revenue": THEME_COLORS["dark_green"],
            "profit": THEME_COLORS["green"]
        }
    )

    fig.update_traces(
        line=dict(
            width=3
        ),

        marker=dict(
            size=8,

            line=dict(
                color="#042722",
                width=2
            )
        ),

        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{fullData.name}: $%{y:,.0f}"
            "<extra></extra>"
        )
    )

    apply_chart_theme(
        fig,
        title="Monthly Revenue & Profit",
        height=450
    )

    fig.update_layout(
        xaxis=dict(
            title=bold_axis_title("Month")
        ),

        yaxis=dict(
            title=bold_axis_title("Amount (USD)"),
            tickprefix="$",
            separatethousands=True
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
        ),

        margin=dict(
            l=75,
            r=45,
            t=100,
            b=75
        )
    )

    return dcc.Graph(
        figure=fig,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# AVERAGE ORDER VALUE
# SQL VIEW: vw_aov_analysis
# ============================================================

def aov_analysis():

    query = """
        SELECT *
        FROM vw_aov_analysis
        ORDER BY year, month
    """

    df = get_data(query)

    fig = px.line(
        df,
        x="year_month",
        y="average_order_value",
        markers=True,
        title="Average Order Value (AOV)"
    )

    fig.update_traces(
        line=dict(
            color=THEME_COLORS["light_mint"],
            width=4
        ),

        marker=dict(
            color=THEME_COLORS["text"],
            size=9,

            line=dict(
                color="#042722",
                width=2
            )
        ),

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average Order Value: $%{y:,.2f}"
            "<extra></extra>"
        )
    )

    apply_chart_theme(
        fig,
        title="Average Order Value (AOV)",
        height=450
    )

    fig.update_layout(
        xaxis=dict(
            title=bold_axis_title("Month")
        ),

        yaxis=dict(
            title=bold_axis_title("Average Order Value (USD)"),
            tickprefix="$"
        ),

        hovermode="x unified",

        margin=dict(
            l=75,
            r=45,
            t=100,
            b=75
        )
    )

    return dcc.Graph(
        figure=fig,
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# REVENUE PAGE
# ============================================================

def revenue_page():

    # ========================================================
    # GET SUMMARY DATA
    # ========================================================

    revenue_query = """
        SELECT
            SUM(price_usd) AS total_revenue,
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(price_usd - cogs_usd) AS total_profit
        FROM orders
    """

    revenue_df = get_data(revenue_query)

    total_revenue = float(
        revenue_df.loc[0, "total_revenue"]
    )

    total_orders = int(
        revenue_df.loc[0, "total_orders"]
    )

    total_profit = float(
        revenue_df.loc[0, "total_profit"]
    )

    aov = (
        total_revenue / total_orders
        if total_orders > 0
        else 0
    )

    gross_margin = (
        total_profit / total_revenue * 100
        if total_revenue > 0
        else 0
    )

    # ========================================================
    # REVENUE PAGE LAYOUT
    # ========================================================

    return html.Div(
        [

            # =================================================
            # PAGE HEADER
            # =================================================

            html.Div(
                [

                    html.H1(
                        "Sales & Revenue Insights",
                        className="page-title"
                    ),

                    html.P(
                        "Revenue trends, sales performance and profitability.",
                        className="page-description"
                    )

                ],

                className="page-header"
            ),

            # =================================================
            # KPI CARDS WITH ICONS
            # =================================================

            html.Div(
                [

                    # TOTAL REVENUE
                    kpi_card(
                        title="Total Revenue",
                        value=f"${total_revenue:,.0f}",
                        icon="lucide:chart-no-axes-column-increasing",
                        icon_class="revenue-icon"
                    ),

                    # TOTAL ORDERS
                    kpi_card(
                        title="Total Orders",
                        value=f"{total_orders:,}",
                        icon="lucide:shopping-cart",
                        icon_class="orders-icon"
                    ),

                    # AVERAGE ORDER VALUE
                    kpi_card(
                        title="Average Order Value",
                        value=f"${aov:,.2f}",
                        icon="lucide:tag",
                        icon_class="aov-icon"
                    ),

                    # GROSS PROFIT
                    kpi_card(
                        title="Gross Profit",
                        value=f"${total_profit:,.0f}",
                        icon="lucide:coins",
                        icon_class="profit-icon"
                    ),

                    # GROSS MARGIN
                    kpi_card(
                        title="Gross Margin",
                        value=f"{gross_margin:.2f}%",
                        icon="lucide:percent",
                        icon_class="margin-icon"
                    )

                ],

                className="kpi-container"
            ),

            # =================================================
            # REVENUE TRENDS
            # =================================================

            html.H2(
                "Revenue Trends",
                className="section-title"
            ),

            html.P(
                "Understand annual revenue contribution and month-over-month growth.",
                className="section-description"
            ),

            html.Div(
                [

                    # YEARLY REVENUE
                    html.Div(
                        [
                            yearly_revenue()
                        ],
                        className="chart-half"
                    ),

                    # MONTH-OVER-MONTH GROWTH
                    html.Div(
                        [
                            mom_revenue_growth()
                        ],
                        className="chart-half"
                    )

                ],

                className="chart-row"
            ),

            # =================================================
            # SALES AND PROFITABILITY
            # =================================================

            html.H2(
                "Sales & Profitability",
                className="section-title"
            ),

            html.P(
                "Track average order value alongside monthly revenue and profit performance.",
                className="section-description"
            ),

            html.Div(
                [

                    # AVERAGE ORDER VALUE
                    html.Div(
                        [
                            aov_analysis()
                        ],
                        className="chart-half"
                    ),

                    # MONTHLY REVENUE AND PROFIT
                    html.Div(
                        [
                            monthly_revenue_profit()
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