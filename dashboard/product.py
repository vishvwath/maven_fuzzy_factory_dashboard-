from dash import html, dcc
from dash_iconify import DashIconify
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
    "medium_green": "#6EE7B7",
    "soft_green": "#047857",
    "white": "#F0FDF4",
    "text": "#D1FAE5",
    "muted_text": "#94A3B8",
    "grid": "rgba(110, 231, 183, 0.12)",
    "border": "#075E54",
    "hover_border": "#10B981",
    "dark_border": "#10B981",
}


# ============================================================
# CHART THEME SETTINGS
# ============================================================

def apply_chart_theme(
    fig,
    title=None,
    height=450,
    left_margin=85,
    right_margin=85,
    top_margin=105,
    bottom_margin=105
):
    """
    Applies the complete Mint Green / Emerald Green theme
    to Plotly charts.
    """

    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(
                    family="Arial",
                    size=22,
                    color="#F0FDF4"
                ),
                x=0.02,
                xanchor="left"
            )
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        font=dict(
            family="Arial",
            color="#D1FAE5",
            size=14
        ),
        height=height,
        margin=dict(
            l=left_margin,
            r=right_margin,
            t=top_margin,
            b=bottom_margin
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#073B34",
            bordercolor=THEME_COLORS["green"],
            font=dict(
                family="Arial",
                size=14,
                color="#F0FDF4"
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                family="Arial",
                size=14,
                color="#F0FDF4"
            ),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=THEME_COLORS["border"],
            borderwidth=1
        ),
        uniformtext=dict(
            minsize=13,
            mode="show"
        )
    )

    fig.update_xaxes(
        showline=True,
        linecolor=THEME_COLORS["border"],
        linewidth=1.5,
        mirror=True,
        gridcolor=THEME_COLORS["grid"],
        zerolinecolor=THEME_COLORS["border"],
        tickfont=dict(
            family="Arial",
            size=14,
            color="#D1FAE5"
        ),
        title_font=dict(
            family="Arial",
            size=17,
            color="#F0FDF4"
        ),
        automargin=True
    )

    fig.update_yaxes(
        showline=True,
        linecolor=THEME_COLORS["border"],
        linewidth=1.5,
        mirror=True,
        gridcolor=THEME_COLORS["grid"],
        zerolinecolor=THEME_COLORS["border"],
        tickfont=dict(
            family="Arial",
            size=14,
            color="#D1FAE5"
        ),
        title_font=dict(
            family="Arial",
            size=17,
            color="#F0FDF4"
        ),
        automargin=True
    )

    return fig


# ============================================================
# KPI ICON COLORS
# ============================================================

KPI_ICON_THEME = {
    "orders-icon": {
        "icon": THEME_COLORS["green"],
        "background": "#073B34",
        "accent": THEME_COLORS["green"]
    },
    "revenue-icon": {
        "icon": THEME_COLORS["green"],
        "background": "#073B34",
        "accent": THEME_COLORS["green"]
    },
    "aov-icon": {
        "icon": THEME_COLORS["green"],
        "background": "#073B34",
        "accent": THEME_COLORS["green"]
    },
    "profit-icon": {
        "icon": THEME_COLORS["green"],
        "background": "#073B34",
        "accent": THEME_COLORS["green"]
    },
    "margin-icon": {
        "icon": THEME_COLORS["green"],
        "background": "#073B34",
        "accent": THEME_COLORS["green"]
    }
}


# ============================================================
# KPI CARD WITH ICON
# ============================================================

def kpi_card(title, value, icon, icon_class):
    icon_colors = KPI_ICON_THEME.get(
        icon_class,
        {
            "icon": THEME_COLORS["green"],
            "background": "transparent",
            "accent": THEME_COLORS["green"]
        }
    )

    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        title,
                        className="product-kpi-title",
                        style={
                            "margin": "10px 0 10px 0",
                            "color": "#79A99E",
                            "fontSize": "10px",
                            "fontWeight": "800",
                            "lineHeight": "1.25",
                            "letterSpacing": "0.8px"
                        }
                    ),
                    html.H2(
                        value,
                        className="product-kpi-value",
                        style={
                            "margin": "0",
                            "color": "#F2FFF9",
                            "fontFamily": '"Elsie", Georgia, serif',
                            "fontSize": "29px",
                            "fontWeight": "800",
                            "lineHeight": "1.15",
                            "whiteSpace": "nowrap"
                        }
                    )
                ],
                className="product-kpi-content",
                style={
                    "display": "block",
                    "width": "100%",
                    "minWidth": "0",
                    "padding": "0 78px 0 0",
                    "margin": "0",
                    "boxSizing": "border-box"
                }
            ),

            html.Div(
                [
                    DashIconify(
                        icon=icon,
                        width=26,
                        height=26,
                        color="#D1FAE5"
                    )
                ],
                className=f"product-kpi-icon {icon_class}",
                style={
                    "position": "absolute",
                    "top": "20px",
                    "right": "20px",
                    "width": "40px",
                    "height": "40px",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "0",
                    "margin": "0",
                    "backgroundColor": "transparent",
                    "border": "none",
                    "borderRadius": "0",
                    "boxShadow": "none",
                    "boxSizing": "border-box"
                }
            )
        ],
        className="product-kpi-card",
        style={
            "position": "relative",
            "display": "block",
            "width": "100%",
            "minWidth": "0",
            "height": "165px",
            "minHeight": "165px",
            "padding": "20px",
            "margin": "0",
            "backgroundColor": "#062F2A",
            "border": f"1px solid {THEME_COLORS['border']}",
            "borderRadius": "13px",
            "boxShadow": "0 7px 22px rgba(0,0,0,0.15)",
            "overflow": "hidden",
            "boxSizing": "border-box"
        }
    )


# ============================================================
# KPI ICONS
# ============================================================

ICON_ORDERS = "lucide:shopping-cart"
ICON_REVENUE = "lucide:chart-no-axes-column-increasing"
ICON_NET_REVENUE = "lucide:wallet"
ICON_PROFIT = "lucide:coins"
ICON_REFUND = "lucide:refresh-ccw"


# ============================================================
# BOLD AXIS TITLE HELPER
# ============================================================

def bold_axis_title(text):
    return dict(
        text=f"<b>{text}</b>",
        font=dict(
            family="Arial",
            size=17,
            color="#F0FDF4"
        )
    )


# ============================================================
# PRODUCT PAGE
# ============================================================

def product_page():

    # ========================================================
    # 1. PRODUCT KPI DATA
    # ========================================================

    product_kpi = get_data(
        """
        SELECT *
        FROM vw_kpi_product
        """
    )

    total_orders = product_kpi["orders"].sum()
    total_revenue = product_kpi["revenue"].sum()
    total_net_revenue = product_kpi["net_revenue"].sum()
    total_profit = product_kpi["gross_profit"].sum()
    total_refund_revenue = product_kpi["refund_revenue"].sum()

    # ========================================================
    # 2. PRODUCT PROFITABILITY
    # ========================================================

    profitability_df = get_data(
        """
        SELECT *
        FROM vw_product_profitability
        """
    )

    profitability_df = profitability_df.sort_values(
        by="net_profit",
        ascending=False
    )

    # ========================================================
    # 3. PRODUCT CROSS-SELL
    # ========================================================

    cross_sell_df = get_data(
        """
        SELECT *
        FROM vw_product_cross_sell
        """
    )

    cross_sell_df = cross_sell_df.sort_values(
        by="orders_together",
        ascending=False
    )

    # ========================================================
    # 4. PRIMARY VS CROSS-SOLD
    # ========================================================

    primary_cross_df = get_data(
        """
        SELECT *
        FROM vw_primary_vs_cross_sold
        """
    )

    primary_cross_df = primary_cross_df.sort_values(
        by="cross_sell_rate",
        ascending=False
    )

    # ========================================================
    # 5. REFUND ANALYSIS
    # ========================================================

    refund_df = get_data(
        """
        SELECT *
        FROM vw_product_refund_analysis
        """
    )

    # ========================================================
    # 6. PRODUCT PAGE PERFORMANCE
    # ========================================================

    product_page_df = get_data(
        """
        SELECT *
        FROM _product_page_performance_metrics
        """
    )

    # ========================================================
    # NET REVENUE VS NET PROFIT CHART
    # ========================================================

    revenue_profit_chart = go.Figure()

    revenue_profit_chart.add_trace(
        go.Bar(
            x=profitability_df["product_name"],
            y=profitability_df["net_revenue"],
            name="Net Revenue",
            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=profitability_df["net_revenue"],
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Net Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    revenue_profit_chart.add_trace(
        go.Bar(
            x=profitability_df["product_name"],
            y=profitability_df["net_profit"],
            name="Net Profit",
            marker=dict(
                color=THEME_COLORS["medium_green"],
                line=dict(
                    color="#34D399",
                    width=1
                )
            ),
            text=profitability_df["net_profit"],
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Net Profit: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    revenue_profit_chart.add_trace(
        go.Scatter(
            x=profitability_df["product_name"],
            y=profitability_df["net_profit_pct"],
            name="Net Profit Margin",
            mode="lines+markers+text",
            text=profitability_df["net_profit_pct"],
            texttemplate="%{text:.2f}%",
            textposition="top center",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            yaxis="y2",
            line=dict(
                color="#F0FDF4",
                width=4
            ),
            marker=dict(
                size=11,
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color="#F0FDF4",
                    width=2
                )
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Net Profit Margin: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    revenue_profit_chart.update_layout(
        title=dict(
            text="Net Revenue vs Net Profit by Product",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Product"),
            type="category",
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Amount ($)"),
            tickprefix="$",
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis2=dict(
            title=bold_axis_title("Net Profit Margin (%)"),
            overlaying="y",
            side="right",
            ticksuffix="%",
            range=[50, 71],
            tickmode="linear",
            dtick=3,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#34D399"
            ),
            showline=True,
            linecolor=THEME_COLORS["border"],
            automargin=True
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
                family="Arial",
                size=14,
                color="#F0FDF4"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=85,
            r=115,
            t=105,
            b=105
        ),
        height=500
    )

    apply_chart_theme(
        revenue_profit_chart,
        height=500,
        left_margin=85,
        right_margin=115,
        top_margin=105,
        bottom_margin=105
    )

    # ========================================================
    # PRODUCT PAGE PERFORMANCE CHART
    # ========================================================

    product_page_chart = go.Figure()

    product_page_chart.add_trace(
        go.Bar(
            x=product_page_df["pageview_url"],
            y=product_page_df["sessions"],
            name="Sessions",
            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=product_page_df["sessions"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Sessions: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    product_page_chart.add_trace(
        go.Bar(
            x=product_page_df["pageview_url"],
            y=product_page_df["orders"],
            name="Orders",
            marker=dict(
                color=THEME_COLORS["medium_green"],
                line=dict(
                    color="#34D399",
                    width=1
                )
            ),
            text=product_page_df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Orders: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    product_page_chart.add_trace(
        go.Scatter(
            x=product_page_df["pageview_url"],
            y=product_page_df["conversion_rate"],
            name="Conversion Rate",
            mode="lines+markers+text",
            text=product_page_df["conversion_rate"],
            texttemplate="%{text:.2f}%",
            textposition="top center",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            yaxis="y2",
            line=dict(
                color="#F0FDF4",
                width=4
            ),
            marker=dict(
                size=10,
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color="#F0FDF4",
                    width=2
                )
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Conversion Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    product_page_chart.update_layout(
        title=dict(
            text="Product Page Performance",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Pageview URL"),
            type="category",
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Sessions / Orders"),
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis2=dict(
            title=bold_axis_title("Conversion Rate (%)"),
            overlaying="y",
            side="right",
            ticksuffix="%",
            tickfont=dict(
                family="Arial",
                size=14,
                color="#34D399"
            ),
            showline=True,
            linecolor=THEME_COLORS["border"],
            automargin=True
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
                family="Arial",
                size=14,
                color="#F0FDF4"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=85,
            r=115,
            t=105,
            b=105
        ),
        height=500
    )

    apply_chart_theme(
        product_page_chart,
        height=500,
        left_margin=85,
        right_margin=115,
        top_margin=105,
        bottom_margin=105
    )

    # ========================================================
    # ORDERS BY PRODUCT
    # ========================================================

    orders_df = profitability_df.sort_values(
        by="orders",
        ascending=True
    )

    orders_chart = go.Figure()

    orders_chart.add_trace(
        go.Bar(
            x=orders_df["orders"],
            y=orders_df["product_name"],
            orientation="h",
            name="Orders",
            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=orders_df["orders"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Orders: %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    orders_chart.update_layout(
        title=dict(
            text="Orders by Product",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Orders"),
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Product"),
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=150,
            r=80,
            t=95,
            b=70
        ),
        height=450
    )

    apply_chart_theme(
        orders_chart,
        height=450,
        left_margin=150,
        right_margin=80,
        top_margin=95,
        bottom_margin=70
    )

    # ========================================================
    # PRIMARY VS CROSS-SOLD REVENUE
    # ========================================================

    primary_cross_chart = go.Figure()

    primary_cross_chart.add_trace(
        go.Bar(
            x=primary_cross_df["product_name"],
            y=primary_cross_df["primary_revenue"],
            name="Primary Revenue",
            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=primary_cross_df["primary_revenue"],
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Primary Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    primary_cross_chart.add_trace(
        go.Bar(
            x=primary_cross_df["product_name"],
            y=primary_cross_df["cross_sold_revenue"],
            name="Cross-Sold Revenue",
            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color="#34D399",
                    width=1
                )
            ),
            text=primary_cross_df["cross_sold_revenue"],
            texttemplate="$%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Cross-Sold Revenue: $%{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    primary_cross_chart.update_layout(
        title=dict(
            text="Primary vs Cross-Sold Revenue",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Product"),
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Revenue ($)"),
            tickprefix="$",
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
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
                family="Arial",
                size=14,
                color="#F0FDF4"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=75,
            r=60,
            t=95,
            b=105
        ),
        height=450
    )

    apply_chart_theme(
        primary_cross_chart,
        height=450,
        left_margin=75,
        right_margin=60,
        top_margin=95,
        bottom_margin=105
    )

    # ========================================================
    # PRODUCT CROSS-SELL ANALYSIS
    # ========================================================

    cross_sell_df["product_pair"] = (
        cross_sell_df["product_1_id"].astype(str)
        + " + "
        + cross_sell_df["product_2_id"].astype(str)
    )

    cross_sell_chart_df = cross_sell_df.sort_values(
        by="orders_together",
        ascending=True
    )

    cross_sell_chart = go.Figure()

    cross_sell_chart.add_trace(
        go.Bar(
            x=cross_sell_chart_df["orders_together"],
            y=cross_sell_chart_df["product_pair"],
            orientation="h",
            name="Orders Together",
            marker=dict(
                color=THEME_COLORS["medium_green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=cross_sell_chart_df["orders_together"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Orders Together: %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    cross_sell_chart.update_layout(
        title=dict(
            text="Product Cross-Sell Analysis",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Orders Together"),
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Product Pair"),
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=190,
            r=80,
            t=95,
            b=70
        ),
        height=500
    )

    apply_chart_theme(
        cross_sell_chart,
        height=500,
        left_margin=190,
        right_margin=80,
        top_margin=95,
        bottom_margin=70
    )

    # ========================================================
    # REFUND PORTFOLIO ANALYSIS
    # ========================================================

    refund_chart = go.Figure()

    refund_chart.add_trace(
        go.Bar(
            x=refund_df["product_name"],
            y=refund_df["items_sold"],
            name="Items Sold",
            marker=dict(
                color=THEME_COLORS["green"],
                line=dict(
                    color="#F0FDF4",
                    width=1
                )
            ),
            text=refund_df["items_sold"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Items Sold: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    refund_chart.add_trace(
        go.Bar(
            x=refund_df["product_name"],
            y=refund_df["refunded_items"],
            name="Refunded Items",
            marker=dict(
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color="#34D399",
                    width=1
                )
            ),
            text=refund_df["refunded_items"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            textfont=dict(
                family="Arial",
                size=15,
                color="#F0FDF4"
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Refunded Items: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    refund_chart.add_trace(
        go.Scatter(
            x=refund_df["product_name"],
            y=refund_df["refund_rate_pct"],
            name="Refund Rate",
            mode="lines+markers+text",
            text=refund_df["refund_rate_pct"],
            texttemplate="%{text:.2f}%",
            textposition="top left",
            textfont=dict(
                family="Arial",
                size=16,
                color="#F0FDF4"
            ),
            yaxis="y2",
            line=dict(
                color="#F0FDF4",
                width=4
            ),
            marker=dict(
                size=11,
                color=THEME_COLORS["light_mint"],
                line=dict(
                    color="#F0FDF4",
                    width=2
                )
            ),
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Refund Rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    refund_chart.update_layout(
        title=dict(
            text="Refund Portfolio Analysis",
            font=dict(
                family="Arial",
                size=21,
                color="#F0FDF4"
            ),
            x=0.02,
            xanchor="left"
        ),
        xaxis=dict(
            title=bold_axis_title("Product"),
            type="category",
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis=dict(
            title=bold_axis_title("Items Sold / Refunded Items"),
            separatethousands=True,
            tickfont=dict(
                family="Arial",
                size=14,
                color="#D1FAE5"
            )
        ),
        yaxis2=dict(
            title=bold_axis_title("Refund Rate (%)"),
            overlaying="y",
            side="right",
            ticksuffix="%",
            tickfont=dict(
                family="Arial",
                size=14,
                color="#34D399"
            ),
            showline=True,
            linecolor=THEME_COLORS["border"],
            automargin=True
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
                family="Arial",
                size=14,
                color="#F0FDF4"
            )
        ),
        paper_bgcolor="#042722",
        plot_bgcolor="#062F2A",
        margin=dict(
            l=80,
            r=135,
            t=105,
            b=105
        ),
        height=470
    )

    apply_chart_theme(
        refund_chart,
        height=470,
        left_margin=80,
        right_margin=135,
        top_margin=105,
        bottom_margin=105
    )

    # ========================================================
    # SHARED PAGE STYLES
    # ========================================================

    section_title_style = {
        "color": "#F0FDF4",
        "fontWeight": "800",
        "marginTop": "28px",
        "marginBottom": "8px"
    }

    section_description_style = {
        "color": "#94A3B8",
        "fontSize": "15px",
        "marginBottom": "18px"
    }

    chart_card_style = {
        "backgroundColor": "#062F2A",
        "border": f"1px solid {THEME_COLORS['border']}",
        "borderRadius": "16px",
        "boxShadow": "0 8px 24px rgba(0, 0, 0, 0.30)",
        "overflow": "hidden"
    }

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
                        "Product Insights",
                        className="page-title",
                        style={
                            "color": "#F0FDF4",
                            "fontWeight": "800"
                        }
                    ),

                    html.P(
                        (
                            "Analyze product sales, profitability, "
                            "cross-selling and refund performance."
                        ),
                        className="page-description",
                        style={
                            "color": THEME_COLORS["text"],
                            "fontSize": "16px"
                        }
                    )
                ],
                className="page-header",
                style={
                    "borderBottom": f"1px solid {THEME_COLORS['border']}",
                    "paddingBottom": "18px"
                }
            ),

            # ==================================================
            # KPI CARDS
            # ==================================================

            html.Div(
                [
                    kpi_card(
                        "Total Product Orders",
                        f"{total_orders:,.0f}",
                        ICON_ORDERS,
                        "orders-icon"
                    ),

                    kpi_card(
                        "Total Revenue",
                        f"${total_revenue:,.0f}",
                        ICON_REVENUE,
                        "revenue-icon"
                    ),

                    kpi_card(
                        "Net Revenue",
                        f"${total_net_revenue:,.0f}",
                        ICON_NET_REVENUE,
                        "net-revenue-icon"
                    ),

                    kpi_card(
                        "Gross Profit",
                        f"${total_profit:,.0f}",
                        ICON_PROFIT,
                        "profit-icon"
                    ),

                    kpi_card(
                        "Refund Revenue",
                        f"${total_refund_revenue:,.0f}",
                        ICON_REFUND,
                        "refund-icon"
                    )
                ],
                className="kpi-container"
            ),

            # ==================================================
            # PRODUCT SALES & PROFITABILITY
            # ==================================================

            html.H2(
                "Product Sales & Profitability",
                className="section-title",
                style=section_title_style
            ),

            html.P(
                (
                    "Compare net revenue, net profit and net "
                    "profit margin across products."
                ),
                className="section-description",
                style=section_description_style
            ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                figure=revenue_profit_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-card chart-half",
                        style=chart_card_style
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                figure=product_page_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-card chart-half",
                        style=chart_card_style
                    )
                ],
                className="chart-row"
            ),

            # ==================================================
            # PRODUCT ORDERS & CROSS-SELL
            # ==================================================

            html.H2(
                "Product Orders & Cross-Sell",
                className="section-title",
                style=section_title_style
            ),

            html.P(
                (
                    "Understand product demand and the contribution "
                    "of primary and cross-sold revenue."
                ),
                className="section-description",
                style=section_description_style
            ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                figure=orders_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-card chart-half",
                        style=chart_card_style
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                figure=primary_cross_chart,
                                config={
                                    "displayModeBar": False,
                                    "responsive": True
                                }
                            )
                        ],
                        className="chart-card chart-half",
                        style=chart_card_style
                    )
                ],
                className="chart-row"
            ),

            # ==================================================
            # PRODUCT CROSS-SELL ANALYSIS
            # ==================================================

            html.H2(
                "Product Cross-Sell Analysis",
                className="section-title",
                style=section_title_style
            ),

            html.P(
                (
                    "Identify product combinations that are most "
                    "frequently purchased together."
                ),
                className="section-description",
                style=section_description_style
            ),

            html.Div(
                [
                    dcc.Graph(
                        figure=cross_sell_chart,
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        }
                    )
                ],
                className="chart-card",
                style=chart_card_style
            ),

            # ==================================================
            # REFUND PORTFOLIO ANALYSIS
            # ==================================================

            html.H2(
                "Refund Portfolio Analysis",
                className="section-title",
                style=section_title_style
            ),

            html.P(
                "Analyze product refund performance.",
                className="section-description",
                style=section_description_style
            ),

            html.Div(
                [
                    dcc.Graph(
                        figure=refund_chart,
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        }
                    )
                ],
                className="chart-card",
                style=chart_card_style
            )
        ],
        className="content",
        style={
            "backgroundColor": "#031F1C",
            "color": "#D1FAE5",
            "minHeight": "100vh",
            "paddingBottom": "30px"
        }
    )