USE ECOMMERCE;

##-------------------REVENUE & SALES -------------------------##

### Yearly Revenue Trend 

	CREATE OR REPLACE VIEW vw_yearly_revenue AS
	SELECT
		DATE_FORMAT(created_at, '%Y') AS Year,
		SUM(price_usd) AS Yearly_revenue
	FROM orders
	GROUP BY DATE_FORMAT(created_at, '%Y')
	ORDER BY Year;

	## Month-over-Month (MoM) Revenue Growth

	CREATE OR REPLACE VIEW vw_mom_revenue_growth AS

	WITH monthly_revenue AS (
		SELECT
			DATE_FORMAT(created_at, '%Y-%m') AS month,
			SUM(price_usd) AS revenue
		FROM orders
		GROUP BY DATE_FORMAT(created_at, '%Y-%m')
	)

	SELECT
		month,
		revenue,
		LAG(revenue) OVER (
			ORDER BY month
		) AS previous_month_revenue,

		ROUND(
			(revenue - LAG(revenue) OVER (ORDER BY month))
			/ LAG(revenue) OVER (ORDER BY month) * 100,
			2
		) AS growth_percentage

	FROM monthly_revenue;

	SELECT 
		CASE
			WHEN http_referer IN ('https://www.gsearch.com', 'https://www.bsearch.com') THEN 'organic_search'
			WHEN utm_campaign = 'nonbrand' THEN 'paid_nonbrand' 
			WHEN utm_campaign = 'brand' THEN 'paid_brand' 
			WHEN utm_source IS NULL AND http_referer IS NULL THEN 'direct_type_in' 
			WHEN utm_source = 'social_book' THEN 'paid_social' 
			ELSE 'unknown'
		END AS channel_group,
		COUNT(DISTINCT CASE WHEN is_repeat_session = 0 THEN website_session_id ELSE NULL END) AS new_sessions,
		COUNT(DISTINCT CASE WHEN is_repeat_session = 1 THEN website_session_id ELSE NULL END) AS repeat_sessions
	FROM
		website_sessions
	GROUP BY
		1;
        
        
	##monthly_revenue_performance 

	CREATE OR REPLACE VIEW vw_monthly_revenue_profit AS
	SELECT
		YEAR(created_at) AS year,
		MONTH(created_at) AS month_number,
		DATE_FORMAT(created_at, '%b') AS month,
		
		SUM(price_usd) AS revenue,
		
		SUM(price_usd - cogs_usd) AS profit

	FROM orders

	GROUP BY
		YEAR(created_at),
		MONTH(created_at),
		DATE_FORMAT(created_at, '%b');
        
        
	## Average Order Value Analysis

	CREATE OR REPLACE VIEW vw_aov_analysis AS

	SELECT
		YEAR(created_at) AS year,

		MONTH(created_at) AS month,

		DATE_FORMAT(
			created_at,
			'%Y-%m'
		) AS 'year_month',

		COUNT(DISTINCT order_id) AS orders,

		ROUND(
			SUM(price_usd),
			2
		) AS revenue,

		ROUND(
			SUM(price_usd)
			/
			NULLIF(COUNT(DISTINCT order_id), 0),
			2
		) AS average_order_value

	FROM orders

	GROUP BY
		YEAR(created_at),
		MONTH(created_at),
		DATE_FORMAT(created_at, '%Y-%m');

##---------------------------------MARKETING ANALYSIS-------------------------------------##
 
	##campaign performance 

	CREATE OR REPLACE VIEW vw_campaign_performance AS
	SELECT
		ws.utm_source as Search_Engine,
		ws.utm_campaign as Campaigns,

		COUNT(DISTINCT ws.website_session_id) AS sessions,

		COUNT(DISTINCT o.order_id) AS orders,

		SUM(o.price_usd) AS revenue,

		ROUND(
			COUNT(DISTINCT o.order_id)
			/ NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
			2
		) AS conversion_rate

	FROM website_sessions ws

	LEFT JOIN orders o
		ON ws.website_session_id = o.website_session_id

	GROUP BY
		ws.utm_source,
		ws.utm_campaign;
		
	##device_performance 
		
	CREATE OR REPLACE VIEW vw_device_performance AS
	SELECT
		ws.device_type,

		COUNT(DISTINCT ws.website_session_id) AS sessions,
		COUNT(DISTINCT o.order_id) AS orders,
		SUM(o.price_usd) AS revenue,
		ROUND(
			COUNT(DISTINCT o.order_id)
			/ NULLIF(COUNT(DISTINCT ws.website_session_id), 0) * 100,
			2
		) AS conversion_rate

	FROM website_sessions ws

	LEFT JOIN orders o
		ON ws.website_session_id = o.website_session_id

	GROUP BY ws.device_type;

##------------------------------------WEBSITE------------------------------------------###
	
	##Website_Funnel_analysis

	CREATE OR REPLACE VIEW vw_website_funnel AS

	WITH session_funnel AS (

		SELECT
			 website_session_id,

			MAX(CASE WHEN pageview_url = '/products' THEN 1 ELSE 0 END) AS viewed_products,

			MAX(CASE WHEN pageview_url IN (
						'/the-original-mr-fuzzy',
						'/the-forever-love-bear',
						'/the-birthday-sugar-panda',
						'/the-hudson-river-mini-bear'
					)
					THEN 1 ELSE 0
				END
			) AS viewed_product,

			MAX(
				CASE
					WHEN pageview_url = '/cart'
					THEN 1 ELSE 0
				END
			) AS viewed_cart,

			MAX(
				CASE
					WHEN pageview_url = '/shipping'
					THEN 1 ELSE 0
				END
			) AS viewed_shipping,

			MAX(
				CASE
					WHEN pageview_url IN ('/billing', '/billing-2')
					THEN 1 ELSE 0
				END
			) AS viewed_billing,

			MAX(
				CASE
					WHEN pageview_url = '/thank-you-for-your-order'
					THEN 1 ELSE 0
				END
			) AS completed_order

		FROM website_pageviews

		GROUP BY website_session_id
	)

	SELECT

		COUNT(*) AS Landing,
		SUM(viewed_products) AS Products,
		SUM(viewed_product) AS Product_detail,
		SUM(viewed_cart) AS Cart,
		SUM(viewed_shipping) AS Shipping,
		SUM(viewed_billing) AS Billing,
		SUM(completed_order) AS Completed_Orders
	FROM session_funnel;
    
    ##bounce_rate_analysis

	CREATE OR REPLACE VIEW vw_bounce_rate_analysis AS
	WITH session_pages AS
	(
	SELECT website_session_id,
	MIN(website_pageview_id) first_page,
	COUNT(*) total_pages
	FROM website_pageviews
	GROUP BY website_session_id
	)

	SELECT
	wp.pageview_url landing_page,
	COUNT(*) sessions,
	SUM(CASE WHEN total_pages=1 THEN 1 ELSE 0 END) bounced_sessions,
	ROUND(
	SUM(CASE WHEN total_pages=1 THEN 1 ELSE 0 END)/COUNT(*)*100,2
	) bounce_rate
	FROM session_pages sp
	JOIN website_pageviews wp
	ON sp.first_page=wp.website_pageview_id
	GROUP BY wp.pageview_url;
    
    ###landing_page_analysis  

		CREATE OR REPLACE VIEW landing_page_analysis AS

		SELECT
			CASE
				WHEN landing_page = '/home' THEN 'Home'
				WHEN landing_page = '/lander-1' THEN 'Lander 1'
				WHEN landing_page = '/lander-2' THEN 'Lander 2'
				WHEN landing_page = '/lander-3' THEN 'Lander 3'
				WHEN landing_page = '/lander-4' THEN 'Lander 4'
				WHEN landing_page = '/lander-5' THEN 'Lander 5'
			END AS landing_page,

			COUNT(DISTINCT website_session_id) AS sessions,

			COUNT(DISTINCT order_id) AS orders,
			
			SUM(revenue) AS revenue,

			ROUND(
				COUNT(DISTINCT order_id) * 100.0
				/ COUNT(DISTINCT website_session_id),
				2
			) AS conversion_rate

		FROM
		(
			SELECT
				ws.website_session_id,

				(
					SELECT wp.pageview_url
					FROM website_pageviews wp
					WHERE wp.website_session_id = ws.website_session_id
					ORDER BY wp.website_pageview_id
					LIMIT 1
				) AS landing_page,

				o.order_id,

				COALESCE(o.price_usd, 0) AS revenue

			FROM website_sessions ws

			LEFT JOIN orders o
				ON ws.website_session_id = o.website_session_id

		) AS session_data

		WHERE landing_page IN ('/home', '/lander-1','/lander-2','/lander-3','/lander-4','/lander-5')

		GROUP BY
			landing_page;
        
	## Monthly Website Traffic

	CREATE OR REPLACE VIEW vw_monthly_website_traffic AS

	SELECT
		YEAR(ws.created_at) AS year,
		MONTH(ws.created_at) AS month,

		DATE_FORMAT(
			ws.created_at,
			'%Y-%m'
		) AS 'year_month',

		COUNT(DISTINCT ws.website_session_id) AS sessions,

		COUNT(DISTINCT ws.user_id) AS users,

		COUNT(DISTINCT o.order_id) AS orders,

		ROUND(
			COUNT(DISTINCT o.order_id)
			/
			NULLIF(COUNT(DISTINCT ws.website_session_id), 0)
			* 100,
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
		YEAR(ws.created_at),
		MONTH(ws.created_at),
		DATE_FORMAT(ws.created_at, '%Y-%m');

##-----------------------------------CUSTOMER ANALYSIS---------------------------------------## 
	
	## new vs returning customers 
		
	CREATE OR REPLACE VIEW new_vs_returning_customers AS
SELECT
    CASE
        WHEN s.is_repeat_session = 1 THEN 'Returning'
        ELSE 'New'
    END AS customer_type,

    COUNT(*) AS sessions,

    SUM(COALESCE(o.orders, 0)) AS orders,

    SUM(COALESCE(o.revenue, 0)) AS revenue,

    AVG(s.pageviews) AS avg_pageviews

FROM
(
    SELECT
        ws.website_session_id,
        ws.is_repeat_session,
        COUNT(wp.website_pageview_id) AS pageviews

    FROM website_sessions ws

    JOIN website_pageviews wp
        USING (website_session_id)

    GROUP BY
        ws.website_session_id,
        ws.is_repeat_session
) s

LEFT JOIN
(
    SELECT
        website_session_id,
        COUNT(DISTINCT order_id) AS orders,
        SUM(price_usd) AS revenue

    FROM orders

    GROUP BY
        website_session_id
) o
    USING (website_session_id)

GROUP BY
    customer_type;
    
    ## Days Between First and Second Purchase

	CREATE OR REPLACE VIEW vw_repeat_purchase_gap AS

	WITH ranked_orders AS
	(
		SELECT
			user_id,
			order_id,
			created_at,

			ROW_NUMBER() OVER
			(
				PARTITION BY user_id
				ORDER BY created_at, order_id
			) AS order_number

		FROM orders
	),

	first_second AS
	(
		SELECT
			user_id,

			MAX(
				CASE
					WHEN order_number = 1 THEN created_at
				END
			) AS first_order_date,

			MAX(
				CASE
					WHEN order_number = 2 THEN created_at
				END
			) AS second_order_date

		FROM ranked_orders

		WHERE order_number <= 2

		GROUP BY user_id
	)

	SELECT
		COUNT(*) AS repeat_customers,

		ROUND(
			AVG(
				TIMESTAMPDIFF(
					DAY,
					first_order_date,
					second_order_date
				)
			),
			2
		) AS avg_days_to_second_purchase,

		MIN(
			TIMESTAMPDIFF(
				DAY,
				first_order_date,
				second_order_date
			)
		) AS min_days,

		MAX(
			TIMESTAMPDIFF(
				DAY,
				first_order_date,
				second_order_date
			)
		) AS max_days

	FROM first_second

	WHERE second_order_date IS NOT NULL;

##--------------------------------PRODUCT ANALYSIS--------------------------------------------##

    
	## Product Revenue, Profitability & Margin

	CREATE OR REPLACE VIEW vw_product_profitability AS

	WITH product_sales AS (

		SELECT
			p.product_id,
			p.product_name,

			COUNT(DISTINCT oi.order_id) AS orders,

			ROUND(SUM(oi.price_usd), 2) AS revenue,

			ROUND(SUM(oi.cogs_usd), 2) AS cost,

			ROUND(
				SUM(oi.price_usd - oi.cogs_usd),
				2
			) AS gross_profit

		FROM order_items oi

		JOIN products p
			ON oi.product_id = p.product_id

		GROUP BY
			p.product_id,
			p.product_name

	),

	product_refunds AS (

		SELECT
			oi.product_id,

			COUNT(DISTINCT oir.order_id) AS refund_orders,

			ROUND(
				SUM(oir.refund_amount_usd),
				2
			) AS refund_revenue    

		FROM order_item_refunds oir

		JOIN order_items oi
			ON oir.order_item_id = oi.order_item_id

		GROUP BY
			oi.product_id

	)

	SELECT

		ps.product_id,

		ps.product_name,

		ps.orders,

		COALESCE(pr.refund_orders, 0) AS refund_orders,

		ps.revenue,

		COALESCE(pr.refund_revenue, 0) AS refund_revenue,

		ROUND(
			ps.revenue
			- COALESCE(pr.refund_revenue, 0),
			2
		) AS net_revenue,

		ps.cost,

		ps.gross_profit,

		-- Gross Profit %
		ROUND(
			ps.gross_profit
			/ NULLIF(ps.revenue, 0) * 100,
			2
		) AS gross_profit_pct,

		-- Net Profit
		ROUND(
			ps.revenue
			- COALESCE(pr.refund_revenue, 0)
			- ps.cost,
			2
		) AS net_profit,

		-- Net Profit %
		ROUND(
			(
				ps.revenue
				- COALESCE(pr.refund_revenue, 0)
				- ps.cost
			)
			/
			NULLIF(
				ps.revenue
				- COALESCE(pr.refund_revenue, 0),
				0
			) * 100,
			2
		) AS net_profit_pct

	FROM product_sales ps

	LEFT JOIN product_refunds pr
		ON ps.product_id = pr.product_id;    
		
	## Product Cross-Sell / Frequently Bought Together

	CREATE OR REPLACE VIEW vw_product_cross_sell AS

	SELECT
		oi1.product_id AS product_1_id,
		p1.product_name AS product_1,

		oi2.product_id AS product_2_id,
		p2.product_name AS product_2,

		COUNT(DISTINCT oi1.order_id) AS orders_together

	FROM order_items oi1

	JOIN order_items oi2
		ON oi1.order_id = oi2.order_id
		AND oi1.product_id < oi2.product_id

	JOIN products p1
		ON oi1.product_id = p1.product_id

	JOIN products p2
		ON oi2.product_id = p2.product_id

	GROUP BY
		oi1.product_id,
		p1.product_name,
		oi2.product_id,
		p2.product_name;
        
## Primary vs cross sold analysis 

	CREATE OR REPLACE VIEW vw_primary_vs_cross_sold AS

	SELECT
		p.product_id,
		p.product_name,

		COUNT(DISTINCT CASE
			WHEN oi.is_primary_item = 1
			THEN oi.order_id
		END) AS primary_orders,

		COUNT(DISTINCT CASE
			WHEN oi.is_primary_item = 0
			THEN oi.order_id
		END) AS cross_sold_orders,

		ROUND(
			SUM(CASE
				WHEN oi.is_primary_item = 1
				THEN oi.price_usd
				ELSE 0
			END),
			2
		) AS primary_revenue,

		ROUND(
			SUM(CASE
				WHEN oi.is_primary_item = 0
				THEN oi.price_usd
				ELSE 0
			END),
			2
		) AS cross_sold_revenue,

		ROUND(
			COUNT(DISTINCT CASE
				WHEN oi.is_primary_item = 0
				THEN oi.order_id
			END)
			/ NULLIF(COUNT(DISTINCT oi.order_id), 0) * 100,
			2
		) AS cross_sell_rate

	FROM order_items oi

	JOIN products p
		ON oi.product_id = p.product_id

	GROUP BY
		p.product_id,
		p.product_name;
        
	CREATE OR REPLACE VIEW vw_product_refund_analysis AS
SELECT
    p.product_id AS product_id,
    p.product_name AS product_name,

    COUNT(o.order_item_id) AS items_sold,

    COUNT(r.order_item_refund_id) AS refunded_items,

    ROUND(SUM(IFNULL(r.refund_amount_usd, 0)), 2) AS refund_amount,

    ROUND(
        COUNT(r.order_item_refund_id) * 100.0 /
        COUNT(o.order_item_id),
        2
    ) AS refund_rate_pct

FROM products p
JOIN order_items o
    ON p.product_id = o.product_id
LEFT JOIN order_item_refunds r
    ON o.order_item_id = r.order_item_id

GROUP BY
    p.product_id,
    p.product_name;
    
	###product_page_performance

	CREATE OR REPLACE VIEW _product_page_performance_metrics AS

	WITH product_pageviews AS (

		SELECT
			website_pageview_id,
			website_session_id,
			pageview_url

		FROM website_pageviews
		

		WHERE pageview_url IN (
			'/the-original-mr-fuzzy',
			'/the-forever-love-bear',
			'/the-birthday-sugar-panda',
			'/the-hudson-river-mini-bear'
		) 
	),

	product_page_metrics AS (

		SELECT
			pageview_url,
			COUNT(*) AS pageviews,
			COUNT(DISTINCT website_session_id) AS sessions
			FROM product_pageviews
			GROUP BY pageview_url),

	session_orders AS (

		SELECT
			website_session_id,
			COUNT(DISTINCT order_id) AS orders
		FROM orders
		GROUP BY website_session_id
	),

	product_conversion AS (

		SELECT
			pp.pageview_url,
			COUNT(DISTINCT so.website_session_id) AS converting_sessions,
			COALESCE(SUM(so.orders), 0) AS orders
		FROM product_pageviews pp
		LEFT JOIN session_orders so
			ON pp.website_session_id = so.website_session_id
		GROUP BY pp.pageview_url
	)

	SELECT
		pm.pageview_url,pm.pageviews,pm.sessions,
		COALESCE(pc.converting_sessions, 0) AS converting_sessions,
		COALESCE(pc.orders, 0) AS orders,
		ROUND(
			COALESCE(pc.converting_sessions, 0)
			/ NULLIF(pm.sessions, 0) * 100,
			2
		) AS conversion_rate

	FROM product_page_metrics pm

	LEFT JOIN product_conversion pc
		ON pm.pageview_url = pc.pageview_url;
        
##----------------------------A/B TESTING-----------------------------------------------##

##billing_page_ab_test

	CREATE OR REPLACE VIEW billing_ab_test AS

	WITH billing_test AS (

		SELECT
			wp.website_session_id,
			wp.pageview_url AS billing_version,
			o.order_id,
			o.price_usd

		FROM website_pageviews wp

		LEFT JOIN orders o
			ON wp.website_session_id = o.website_session_id

		WHERE wp.created_at > '2012-09-10'
		  AND wp.created_at < '2012-11-10'

		  AND wp.pageview_url IN (
			  '/billing',
			  '/billing-2'
		  )

	)

	SELECT

		CASE
			WHEN billing_version = '/billing'
				THEN 'Control'
			WHEN billing_version = '/billing-2'
				THEN 'Test'
		END AS experiment_group,

		billing_version,

		COUNT(DISTINCT website_session_id) AS sessions,

		COUNT(DISTINCT order_id) AS orders,

		ROUND(
			COUNT(DISTINCT order_id)
			/ COUNT(DISTINCT website_session_id) * 100,
			2
		) AS conversion_rate,

		ROUND(
			COALESCE(SUM(price_usd), 0)
			/ COUNT(DISTINCT website_session_id),
			2
		) AS revenue_per_session

	FROM billing_test

	GROUP BY
		billing_version;    
		
		
	##home lander1 a/b testing

	CREATE OR REPLACE VIEW landing_page_ab_test AS

	WITH first_pageviews AS (

		SELECT
			ws.website_session_id,
			ws.created_at AS session_created_at,
			wp.website_pageview_id,
			wp.pageview_url,
			ROW_NUMBER() OVER (
				PARTITION BY ws.website_session_id
				ORDER BY wp.website_pageview_id
			) AS page_rank

		FROM website_sessions ws

		INNER JOIN website_pageviews wp
			ON ws.website_session_id = wp.website_session_id

		WHERE ws.created_at >= '2012-06-19'
		  AND ws.created_at < '2012-07-29'
		  AND ws.utm_source = 'gsearch'
		  AND ws.utm_campaign = 'nonbrand'
	),

	experiment_sessions AS (

		SELECT
			website_session_id,
			pageview_url AS landing_page

		FROM first_pageviews

		WHERE page_rank = 1
		  AND pageview_url IN ('/home', '/lander-1')
	),

	session_pageviews AS (

		SELECT
			es.website_session_id,
			es.landing_page,
			COUNT(wp.website_pageview_id) AS pageviews

		FROM experiment_sessions es

		INNER JOIN website_pageviews wp
			ON es.website_session_id = wp.website_session_id

		GROUP BY
			es.website_session_id,
			es.landing_page
	),

	session_orders AS (

		SELECT
			website_session_id,
			COUNT(DISTINCT order_id) AS orders

		FROM orders

		GROUP BY website_session_id
	)

	SELECT

		CASE
			WHEN sp.landing_page = '/home'
				THEN 'Control'
			WHEN sp.landing_page = '/lander-1'
				THEN 'Test'
		END AS experiment_group,

		sp.landing_page,

		COUNT(DISTINCT sp.website_session_id) AS sessions,

		COUNT(
			DISTINCT CASE
				WHEN sp.pageviews = 1
				THEN sp.website_session_id
			END
		) AS bounced_sessions,

		ROUND(
			COUNT(
				DISTINCT CASE
					WHEN sp.pageviews = 1
					THEN sp.website_session_id
				END
			)
			/ COUNT(DISTINCT sp.website_session_id) * 100,
			2
		) AS bounce_rate,

		COUNT(
			DISTINCT CASE
				WHEN so.orders > 0
				THEN sp.website_session_id
			END
		) AS converting_sessions,

		COALESCE(
			SUM(so.orders),
			0
		) AS orders,

		ROUND(
			COUNT(
				DISTINCT CASE
					WHEN so.orders > 0
					THEN sp.website_session_id
				END
			)
			/ COUNT(DISTINCT sp.website_session_id) * 100,
			2
		) AS conversion_rate

	FROM session_pageviews sp

	LEFT JOIN session_orders so
		ON sp.website_session_id = so.website_session_id

	GROUP BY
		sp.landing_page;

