use ecommerce;

CREATE TABLE products (
    product_id INT PRIMARY KEY
);

ALTER TABLE products
ADD COLUMN created_at DATETIME,
ADD COLUMN product_name VARCHAR(255);

INSERT INTO products (product_id, created_at, product_name)
VALUES
(1, '2012-03-19 08:00:00', 'The Original Mr. Fuzzy'),
(2, '2013-01-06 13:00:00', 'The Forever Love Bear'),
(3, '2013-12-12 09:00:00', 'The Birthday Sugar Panda'),
(4, '2014-02-05 10:00:00', 'The Hudson River Mini bear');


CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    created_at DATETIME,
    website_session_id INT,
    user_id INT,
    primary_product_id INT,
    items_purchased INT,
    price_usd DECIMAL(10,2),
    cogs_usd DECIMAL(10,2),

    FOREIGN KEY (website_session_id)
        REFERENCES website_sessions(website_session_id),

    FOREIGN KEY (primary_product_id)
        REFERENCES products(product_id)
);

SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/E-Commerce data analysis/orders.csv"
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    created_at DATETIME,
    order_id INT,
    product_id INT,
    is_primary_item TINYINT,
    price_usd DECIMAL(10,2),
    cogs_usd DECIMAL(10,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

SET GLOBAL local_infile = 1;
LOAD DATA LOCAL INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/E-Commerce data analysis/order_items.csv"
INTO TABLE order_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE order_item_refunds (
    order_item_refund_id INT PRIMARY KEY,
    created_at DATETIME,
    order_item_id INT,
    order_id INT,
    refund_amount_usd DECIMAL(10,2),

    FOREIGN KEY (order_item_id)
        REFERENCES order_items(order_item_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);

SET @json = CONVERT(
    LOAD_FILE('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/E-Commerce data analysis/order_item_refunds.json')
    USING utf8mb4
);
INSERT INTO order_item_refunds
(
    order_item_refund_id,
    created_at,
    order_item_id,
    order_id,
    refund_amount_usd
)
SELECT
    order_item_refund_id,
    created_at,
    order_item_id,
    order_id,
    refund_amount_usd
FROM JSON_TABLE(
    @json,
    '$[*]' COLUMNS (
        order_item_refund_id INT PATH '$.order_item_refund_id',
        created_at DATETIME PATH '$.created_at',
        order_item_id INT PATH '$.order_item_id',
        order_id INT PATH '$.order_id',
        refund_amount_usd DECIMAL(10,2) PATH '$.refund_amount_usd'
    )
) AS jt;