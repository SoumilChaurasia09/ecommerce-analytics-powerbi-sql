-- ========================================================
-- MICROSOFT SQL SERVER (T-SQL) SCHEMA & ANALYTICAL VIEWS
-- Project: E-Commerce & Customer Intelligence Analytics
-- ========================================================

IF OBJECT_ID('fact_order_items', 'U') IS NOT NULL DROP TABLE fact_order_items;
IF OBJECT_ID('fact_orders', 'U') IS NOT NULL DROP TABLE fact_orders;
IF OBJECT_ID('dim_products', 'U') IS NOT NULL DROP TABLE dim_products;
IF OBJECT_ID('dim_customers', 'U') IS NOT NULL DROP TABLE dim_customers;

CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    region VARCHAR(50),
    signup_date DATE
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    unit_cost DECIMAL(10,2),
    unit_price DECIMAL(10,2)
);

CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES dim_customers(customer_id),
    order_date DATE,
    shipping_date DATE,
    shipping_cost DECIMAL(10,2),
    payment_method VARCHAR(30),
    order_status VARCHAR(20)
);

CREATE TABLE fact_order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT FOREIGN KEY REFERENCES fact_orders(order_id),
    product_id INT FOREIGN KEY REFERENCES dim_products(product_id),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_amount DECIMAL(10,2),
    net_revenue DECIMAL(10,2)
);

-- BULK INSERT dim_customers FROM 'C:\...\dim_customers.csv' WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');
GO

-- ---------------------------------------------------------
-- VIEW 1: RFM Customer Segmentation
-- ---------------------------------------------------------
CREATE OR ALTER VIEW vw_customer_rfm AS
WITH customer_aggregates AS (
    SELECT 
        o.customer_id,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.net_revenue) AS monetary_value,
        DATEDIFF(day, MAX(o.order_date), (SELECT MAX(order_date) FROM fact_orders)) AS recency_days
    FROM fact_orders o
    JOIN fact_order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY o.customer_id
),
rfm_scores AS (
    SELECT 
        customer_id,
        recency_days,
        total_orders,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY total_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_aggregates
)
SELECT 
    customer_id,
    recency_days,
    total_orders,
    monetary_value,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE 
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'Recent / Promising'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk / Need Attention'
        WHEN r_score <= 1 AND f_score <= 2 THEN 'Lost Customers'
        ELSE 'Potential Loyalist'
    END AS customer_segment
FROM rfm_scores;
GO

-- ---------------------------------------------------------
-- VIEW 2: Monthly Cohort Retention Matrix
-- ---------------------------------------------------------
CREATE OR ALTER VIEW vw_cohort_retention AS
WITH customer_first_order AS (
    SELECT 
        customer_id,
        DATEFROMPARTS(YEAR(MIN(order_date)), MONTH(MIN(order_date)), 1) AS cohort_month
    FROM fact_orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),
customer_monthly_activity AS (
    SELECT DISTINCT
        o.customer_id,
        DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS activity_month
    FROM fact_orders o
    WHERE o.order_status = 'Completed'
),
cohort_progression AS (
    SELECT 
        cfo.cohort_month,
        cma.activity_month,
        DATEDIFF(month, cfo.cohort_month, cma.activity_month) AS cohort_index,
        COUNT(DISTINCT cma.customer_id) AS active_customers
    FROM customer_first_order cfo
    JOIN customer_monthly_activity cma ON cfo.customer_id = cma.customer_id
    GROUP BY cfo.cohort_month, cma.activity_month
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS total_cohort_size
    FROM customer_first_order
    GROUP BY cohort_month
)
SELECT 
    cp.cohort_month,
    cs.total_cohort_size,
    cp.cohort_index,
    cp.active_customers,
    ROUND((CAST(cp.active_customers AS DECIMAL(10,2)) / cs.total_cohort_size) * 100, 2) AS retention_rate_pct
FROM cohort_progression cp
JOIN cohort_sizes cs ON cp.cohort_month = cs.cohort_month;
GO
