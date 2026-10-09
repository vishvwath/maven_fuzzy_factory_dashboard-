use ecommerce;

-- ============================================================
-- MAVEN FUZZY FACTORY - DASHBOARD KPI VIEWS
-- MySQL | Python / Streamlit Dashboard
-- ============================================================
-- Final KPI layer
-- Excludes:
--   * Top Channel
--   * Product Views
--   * All A/B Testing KPIs
-- ============================================================


-- ============================================================
-- 1. EXECUTIVE / REVENUE
-- ============================================================

CREATE OR REPLACE VIEW vw_kpi_executive AS
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(COALESCE(SUM(o.price_usd), 0), 2) AS total_revenue,
    ROUND(
        COALESCE(SUM(o.price_usd), 0)
        / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS average_order_value,
    ROUND(
        COALESCE(SUM(o.price_usd - o.cogs_usd), 0),
        2
    ) AS gross_profit,
    ROUND(
        COALESCE(SUM(o.price_usd - o.cogs_usd), 0)
        / NULLIF(SUM(o.price_usd), 0) * 100,
        2
    ) AS gross_margin_pct,
    COUNT(DISTINCT ws.website_session_id) AS total_sessions,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
        2
    ) AS conversion_rate
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id;


-- ============================================================
-- 2. MARKETING & TRAFFIC
-- ============================================================

CREATE OR REPLACE VIEW vw_kpi_marketing AS
SELECT
    COUNT(DISTINCT ws.website_session_id) AS total_sessions,
    COUNT(DISTINCT ws.user_id) AS total_users,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
        2
    ) AS conversion_rate,
    ROUND(
        COALESCE(SUM(o.price_usd), 0),
        2
    ) AS total_revenue
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id;


CREATE OR REPLACE VIEW vw_kpi_channel AS
SELECT
    CASE
        WHEN ws.http_referer IN (
            'https://www.gsearch.com',
            'https://www.bsearch.com'
        ) THEN 'organic_search'

        WHEN ws.utm_campaign = 'nonbrand'
            THEN 'paid_nonbrand'

        WHEN ws.utm_campaign = 'brand'
            THEN 'paid_brand'

        WHEN ws.utm_source IS NULL
             AND ws.http_referer IS NULL
            THEN 'direct_type_in'

        WHEN ws.utm_source = 'social_book'
            THEN 'paid_social'

        ELSE 'unknown'
    END AS channel_group,

    COUNT(DISTINCT ws.website_session_id) AS sessions,
    COUNT(DISTINCT ws.user_id) AS users,
    COUNT(DISTINCT o.order_id) AS orders,

    ROUND(
        COUNT(DISTINCT o.order_id)
        / NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
        2
    ) AS conversion_rate,

    ROUND(
        COALESCE(SUM(o.price_usd), 0),
        2
    ) AS revenue

FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id

GROUP BY
    CASE
        WHEN ws.http_referer IN (
            'https://www.gsearch.com',
            'https://www.bsearch.com'
        ) THEN 'organic_search'

        WHEN ws.utm_campaign = 'nonbrand'
            THEN 'paid_nonbrand'

        WHEN ws.utm_campaign = 'brand'
            THEN 'paid_brand'

        WHEN ws.utm_source IS NULL
             AND ws.http_referer IS NULL
            THEN 'direct_type_in'

        WHEN ws.utm_source = 'social_book'
            THEN 'paid_social'

        ELSE 'unknown'
    END;


CREATE OR REPLACE VIEW vw_kpi_device AS
SELECT
    ws.device_type,
    COUNT(DISTINCT ws.website_session_id) AS sessions,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(
        COUNT(DISTINCT o.order_id)
        / NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
        2
    ) AS conversion_rate,
    ROUND(
        COALESCE(SUM(o.price_usd), 0),
        2
    ) AS revenue
FROM website_sessions ws
LEFT JOIN orders o
    ON ws.website_session_id = o.website_session_id
GROUP BY ws.device_type;


-- ============================================================
-- 3. WEBSITE & FUNNEL
-- ============================================================

CREATE OR REPLACE VIEW vw_kpi_website AS

WITH funnel AS (
    SELECT
        website_session_id,

        MAX(
            CASE
                WHEN pageview_url IN (
                    '/home',
                    '/lander-1',
                    '/lander-2',
                    '/lander-3',
                    '/lander-4',
                    '/lander-5'
                )
                THEN 1 ELSE 0
            END
        ) AS landing_sessions,

        MAX(
            CASE
                WHEN pageview_url = '/products'
                THEN 1 ELSE 0
            END
        ) AS product_sessions,

        MAX(
            CASE
                WHEN pageview_url IN (
                    '/the-original-mr-fuzzy',
                    '/the-forever-love-bear',
                    '/the-birthday-sugar-panda',
                    '/the-hudson-river-mini-bear'
                )
                THEN 1 ELSE 0
            END
        ) AS product_detail_sessions,

        MAX(
            CASE
                WHEN pageview_url = '/cart'
                THEN 1 ELSE 0
            END
        ) AS cart_sessions,

        MAX(
            CASE
                WHEN pageview_url = '/shipping'
                THEN 1 ELSE 0
            END
        ) AS shipping_sessions,

        MAX(
            CASE
                WHEN pageview_url IN (
                    '/billing',
                    '/billing-2'
                )
                THEN 1 ELSE 0
            END
        ) AS billing_sessions,

        MAX(
            CASE
                WHEN pageview_url = '/thank-you-for-your-order'
                THEN 1 ELSE 0
            END
        ) AS completed_orders

    FROM website_pageviews
    GROUP BY website_session_id
),

pages AS (
    SELECT
        website_session_id,
        COUNT(*) AS page_count
    FROM website_pageviews
    GROUP BY website_session_id
)

SELECT
    COUNT(*) AS total_sessions,

    SUM(landing_sessions) AS landing_sessions,

    SUM(cart_sessions) AS cart_sessions,

    SUM(billing_sessions) AS billing_sessions,

    SUM(completed_orders) AS completed_orders,

    ROUND(
        SUM(completed_orders)
        / NULLIF(COUNT(*), 0) * 100,
        2
    ) AS funnel_conversion_rate,

    ROUND(
        SUM(
            CASE
                WHEN pages.page_count = 1
                THEN 1 ELSE 0
            END
        )
        / NULLIF(COUNT(*), 0) * 100,
        2
    ) AS bounce_rate

FROM funnel
JOIN pages
    ON funnel.website_session_id = pages.website_session_id;


-- ============================================================
-- 4. CUSTOMER
-- ============================================================

CREATE OR REPLACE VIEW vw_kpi_customer AS

SELECT
    customer_type,

    COUNT(DISTINCT website_session_id) AS sessions,

    SUM(orders) AS orders,

    ROUND(
        SUM(revenue),
        2
    ) AS revenue,

    ROUND(
        SUM(orders)
        / NULLIF(COUNT(DISTINCT website_session_id), 0) * 100,
        2
    ) AS conversion_rate,

    ROUND(
        SUM(revenue)
        / NULLIF(SUM(orders), 0),
        2
    ) AS average_order_value

FROM (

    SELECT
        ws.website_session_id,

        CASE
            WHEN ws.is_repeat_session = 1
                THEN 'Returning'
            ELSE 'New'
        END AS customer_type,

        COUNT(DISTINCT o.order_id) AS orders,

        COALESCE(
            SUM(o.price_usd),
            0
        ) AS revenue

    FROM website_sessions ws

    JOIN website_pageviews wp
        ON ws.website_session_id = wp.website_session_id

    LEFT JOIN orders o
        ON ws.website_session_id = o.website_session_id

    GROUP BY
        ws.website_session_id,
        ws.is_repeat_session

) x

GROUP BY customer_type;


CREATE OR REPLACE VIEW vw_kpi_repeat_customer AS

WITH ranked AS (

    SELECT
        user_id,
        created_at,

        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY created_at, order_id
        ) AS rn

    FROM orders
),

first_second AS (

    SELECT
        user_id,

        MAX(
            CASE
                WHEN rn = 1
                THEN created_at
            END
        ) AS first_order,

        MAX(
            CASE
                WHEN rn = 2
                THEN created_at
            END
        ) AS second_order

    FROM ranked

    WHERE rn <= 2

    GROUP BY user_id
)

SELECT
    COUNT(*) AS repeat_customers,

    ROUND(
        AVG(
            TIMESTAMPDIFF(
                DAY,
                first_order,
                second_order
            )
        ),
        2
    ) AS avg_days_to_second_purchase

FROM first_second

WHERE second_order IS NOT NULL;


-- ============================================================
-- 5. PRODUCT
-- ============================================================

CREATE OR REPLACE VIEW vw_kpi_product AS

WITH sales AS (

    SELECT
        p.product_id,
        p.product_name,

        COUNT(DISTINCT oi.order_id) AS orders,

        ROUND(
            SUM(oi.price_usd),
            2
        ) AS revenue,

        ROUND(
            SUM(oi.cogs_usd),
            2
        ) AS cost,

        ROUND(
            SUM(
                oi.price_usd - oi.cogs_usd
            ),
            2
        ) AS gross_profit

    FROM order_items oi

    JOIN products p
        ON oi.product_id = p.product_id

    GROUP BY
        p.product_id,
        p.product_name
),

refunds AS (

    SELECT
        oi.product_id,

        ROUND(
            SUM(oir.refund_amount_usd),
            2
        ) AS refund_revenue

    FROM order_item_refunds oir

    JOIN order_items oi
        ON oir.order_item_id = oi.order_item_id

    GROUP BY oi.product_id
)

SELECT
    s.product_id,
    s.product_name,
    s.orders,

    s.revenue,

    ROUND(
        s.revenue
        - COALESCE(r.refund_revenue, 0),
        2
    ) AS net_revenue,

    s.gross_profit,

    ROUND(
        s.gross_profit
        / NULLIF(s.revenue, 0) * 100,
        2
    ) AS gross_profit_pct,

    COALESCE(
        r.refund_revenue,
        0
    ) AS refund_revenue

FROM sales s

LEFT JOIN refunds r
    ON s.product_id = r.product_id;


-- Cross-sell revenue:
-- Revenue generated by orders containing more than one product.
-- This is calculated at the order level to avoid double-counting
-- individual order-item revenue.

CREATE OR REPLACE VIEW vw_kpi_cross_sell_revenue AS

SELECT
    ROUND(
        COALESCE(
            SUM(
                CASE
                    WHEN product_count > 1
                    THEN order_revenue
                    ELSE 0
                END
            ),
            0
        ),
        2
    ) AS cross_sell_revenue

FROM (

    SELECT
        oi.order_id,

        COUNT(DISTINCT oi.product_id) AS product_count,

        SUM(oi.price_usd) AS order_revenue

    FROM order_items oi

    GROUP BY oi.order_id

) order_summary;