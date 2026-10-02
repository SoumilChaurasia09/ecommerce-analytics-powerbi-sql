import csv
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducible generation
random.seed(42)

BASE_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\ecommerce_bi_project"
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

print("Starting synthetic data generation...")

# ---------------------------------------------------------
# 1. GENERATE DIM_PRODUCTS (40 products across 4 categories)
# ---------------------------------------------------------
products_data = [
    # Electronics
    ("Apex Pro 16-inch Laptop", "Electronics", "Laptops", 850.00, 1299.99),
    ("Zenith Ultrabook 14", "Electronics", "Laptops", 620.00, 949.99),
    ("Pulse ANC Wireless Headphones", "Electronics", "Audio", 65.00, 149.99),
    ("EchoWave Bluetooth Speaker", "Electronics", "Audio", 35.00, 79.99),
    ("Horizon 27-inch 4K Monitor", "Electronics", "Displays", 180.00, 329.99),
    ("Vortex 34-inch Ultrawide Monitor", "Electronics", "Displays", 310.00, 549.99),
    ("Nova Mechanical Gaming Keyboard", "Electronics", "Accessories", 45.00, 99.99),
    ("Precision Wireless Ergonomic Mouse", "Electronics", "Accessories", 22.00, 59.99),
    ("OmniCharge 100W USB-C Dock", "Electronics", "Accessories", 50.00, 119.99),
    ("TrueVision 1080p Streaming Webcam", "Electronics", "Accessories", 28.00, 69.99),

    # Furniture
    ("ErgoFlex Mesh Office Chair", "Furniture", "Seating", 120.00, 249.99),
    ("Titan Executive Leather Chair", "Furniture", "Seating", 190.00, 389.99),
    ("Elevate Dual-Motor Standing Desk", "Furniture", "Desks", 240.00, 499.99),
    ("Compact Studio Desk 48-inch", "Furniture", "Desks", 95.00, 199.99),
    ("ModuStack 4-Tier Bookshelf", "Furniture", "Storage", 70.00, 159.99),
    ("SteelFrame Mobile File Cabinet", "Furniture", "Storage", 55.00, 129.99),
    ("Lumina Balanced Arm Desk Lamp", "Furniture", "Lighting", 18.00, 45.99),
    ("Aura Ambient LED Monitor Light Bar", "Furniture", "Lighting", 24.00, 54.99),
    ("ComfortStep Anti-Fatigue Floor Mat", "Furniture", "Accessories", 15.00, 39.99),
    ("Bamboo Cable Organizer Hub", "Furniture", "Accessories", 8.00, 24.99),

    # Office Supplies
    ("Executive Hardcover Notebook", "Office Supplies", "Stationery", 4.50, 14.99),
    ("Archival Gel Ink Pens (Pack of 12)", "Office Supplies", "Stationery", 5.00, 16.99),
    ("Heavy Duty Desk Stapler & Staples", "Office Supplies", "Stationery", 7.00, 19.99),
    ("Recycled Premium Copy Paper (5 Reams)", "Office Supplies", "Paper", 16.00, 34.99),
    ("Sticky Notes Assorted Pack (12 Pads)", "Office Supplies", "Paper", 3.50, 11.99),
    ("Presentation Display Binders (Pack of 4)", "Office Supplies", "Filing", 8.00, 22.99),
    ("Expanding Accordion File Folder", "Office Supplies", "Filing", 5.50, 15.99),
    ("Magnetic Dry-Erase Whiteboard 36x24", "Office Supplies", "Boards", 22.00, 54.99),
    ("Dual-Action Document Shredder", "Office Supplies", "Equipment", 42.00, 89.99),
    ("Heavy-Duty Label Maker Machine", "Office Supplies", "Equipment", 20.00, 49.99),

    # Apparel & Bags
    ("Commuter Water-Resistant Laptop Backpack", "Apparel & Bags", "Bags", 32.00, 79.99),
    ("Metro Sling Crossbody Tech Bag", "Apparel & Bags", "Bags", 18.00, 45.99),
    ("Weekend Canvas Duffel Bag", "Apparel & Bags", "Bags", 28.00, 69.99),
    ("Classic Organic Cotton Tech Hoodie", "Apparel & Bags", "Clothing", 22.00, 59.99),
    ("Merino Wool Everyday Crewneck", "Apparel & Bags", "Clothing", 35.00, 84.99),
    ("Performance Breathable Polo Shirt", "Apparel & Bags", "Clothing", 14.00, 39.99),
    ("Structured Minimalist Snapback Cap", "Apparel & Bags", "Accessories", 8.00, 24.99),
    ("Insulated Stainless Steel Water Bottle 32oz", "Apparel & Bags", "Accessories", 10.00, 29.99),
    ("Thermal Wool Tech Gloves", "Apparel & Bags", "Accessories", 9.00, 24.99),
    ("Compact Windproof Travel Umbrella", "Apparel & Bags", "Accessories", 7.50, 21.99)
]

products = []
for idx, p in enumerate(products_data, start=101):
    products.append({
        "product_id": idx,
        "product_name": p[0],
        "category": p[1],
        "sub_category": p[2],
        "unit_cost": round(p[3], 2),
        "unit_price": round(p[4], 2)
    })

# Write dim_products.csv
prod_file = os.path.join(DATA_DIR, "dim_products.csv")
with open(prod_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["product_id", "product_name", "category", "sub_category", "unit_cost", "unit_price"])
    writer.writeheader()
    writer.writerows(products)

print(f"Generated {len(products)} products in {prod_file}")

# ---------------------------------------------------------
# 2. GENERATE DIM_CUSTOMERS (600 customers)
# ---------------------------------------------------------
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
    "Christopher", "Nancy", "Daniel", "Margaret", "Matthew", "Lisa", "Anthony", "Betty", "Donald", "Dorothy",
    "Mark", "Sandra", "Paul", "Ashley", "Steven", "Kimberly", "Andrew", "Donna", "Kenneth", "Emily",
    "Joshua", "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Edward", "Deborah",
    "Aarav", "Priya", "Rahul", "Ananya", "Vikram", "Sneha", "Rohan", "Neha", "Arjun", "Pooja",
    "Carlos", "Maria", "Alejandro", "Sofia", "Mateo", "Camila", "Lucas", "Valentina", "Liam", "Emma"
]
last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Sharma", "Patel", "Verma", "Rao", "Gupta", "Mehta", "Singh", "Nair", "Reddy", "Chopra"
]
regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
region_weights = [0.45, 0.28, 0.18, 0.09]

start_date_cust = datetime(2023, 1, 1)
end_date_cust = datetime(2025, 6, 30)
delta_days_cust = (end_date_cust - start_date_cust).days

customers = []
for cid in range(1001, 1601):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 999)}@example.com"
    reg = random.choices(regions, weights=region_weights)[0]
    signup_days = random.randint(0, delta_days_cust)
    signup_dt = (start_date_cust + timedelta(days=signup_days)).date()
    
    customers.append({
        "customer_id": cid,
        "customer_name": name,
        "email": email,
        "region": reg,
        "signup_date": signup_dt.strftime("%Y-%m-%d")
    })

cust_file = os.path.join(DATA_DIR, "dim_customers.csv")
with open(cust_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "customer_name", "email", "region", "signup_date"])
    writer.writeheader()
    writer.writerows(customers)

print(f"Generated {len(customers)} customers in {cust_file}")

# ---------------------------------------------------------
# 3. GENERATE FACT_ORDERS & FACT_ORDER_ITEMS (4,500+ orders)
# ---------------------------------------------------------
payment_methods = ["Credit Card", "PayPal", "Debit Card", "Apple Pay", "Bank Transfer"]
payment_weights = [0.50, 0.25, 0.12, 0.10, 0.03]

status_options = ["Completed", "Returned", "Cancelled"]
status_weights = [0.91, 0.06, 0.03]

orders = []
order_items = []

order_counter = 50001
item_counter = 800001

dataset_end_date = datetime(2026, 6, 30)

# Customer activity profiles:
# 15% VIP/Champions: 10 - 22 orders
# 30% Loyal: 4 - 9 orders
# 35% Occasional/At Risk: 2 - 3 orders
# 20% One-timers: 1 order

for cust in customers:
    cid = cust["customer_id"]
    signup = datetime.strptime(cust["signup_date"], "%Y-%m-%d")
    
    rand_profile = random.random()
    if rand_profile < 0.15:
        num_orders = random.randint(10, 22)
    elif rand_profile < 0.45:
        num_orders = random.randint(4, 9)
    elif rand_profile < 0.80:
        num_orders = random.randint(2, 3)
    else:
        num_orders = 1
        
    days_available = (dataset_end_date - signup).days
    if days_available <= 0:
        days_available = 1

    # First order is shortly after signup (0 to 14 days)
    order_offsets = [random.randint(0, min(14, days_available))]
    
    for _ in range(num_orders - 1):
        order_offsets.append(random.randint(15, days_available))
        
    order_offsets = sorted(list(set(order_offsets))) # unique sorted order dates
    
    for offset in order_offsets:
        order_dt = signup + timedelta(days=offset)
        if order_dt > dataset_end_date:
            continue
            
        ship_days = random.randint(1, 5)
        ship_dt = order_dt + timedelta(days=ship_days)
        
        status = random.choices(status_options, weights=status_weights)[0]
        pay_method = random.choices(payment_methods, weights=payment_weights)[0]
        ship_cost = round(random.choice([0.0, 4.99, 9.99, 14.99]), 2)
        
        cur_order_id = order_counter
        order_counter += 1
        
        orders.append({
            "order_id": cur_order_id,
            "customer_id": cid,
            "order_date": order_dt.strftime("%Y-%m-%d"),
            "shipping_date": ship_dt.strftime("%Y-%m-%d"),
            "shipping_cost": ship_cost,
            "payment_method": pay_method,
            "order_status": status
        })
        
        # Line items: 1 to 4 distinct products per order
        num_items = random.choices([1, 2, 3, 4], weights=[0.45, 0.35, 0.15, 0.05])[0]
        chosen_products = random.sample(products, num_items)
        
        for p in chosen_products:
            qty = random.choices([1, 2, 3, 4, 5], weights=[0.68, 0.20, 0.07, 0.03, 0.02])[0]
            unit_price = p["unit_price"]
            
            # Discounts: 0%, 5%, 10%, 15%, 20%
            disc_rate = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.55, 0.20, 0.15, 0.07, 0.03])[0]
            gross = round(unit_price * qty, 2)
            disc_amount = round(gross * disc_rate, 2)
            net_revenue = round(gross - disc_amount, 2)
            
            order_items.append({
                "order_item_id": item_counter,
                "order_id": cur_order_id,
                "product_id": p["product_id"],
                "quantity": qty,
                "unit_price": unit_price,
                "discount_amount": disc_amount,
                "net_revenue": net_revenue
            })
            item_counter += 1

# Write fact_orders.csv
orders_file = os.path.join(DATA_DIR, "fact_orders.csv")
with open(orders_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "customer_id", "order_date", "shipping_date", "shipping_cost", "payment_method", "order_status"])
    writer.writeheader()
    writer.writerows(orders)

# Write fact_order_items.csv
items_file = os.path.join(DATA_DIR, "fact_order_items.csv")
with open(items_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_amount", "net_revenue"])
    writer.writeheader()
    writer.writerows(order_items)

print(f"Generated {len(orders)} orders in {orders_file}")
print(f"Generated {len(order_items)} order items in {items_file}")

# ---------------------------------------------------------
# 4. GENERATE DDL & SCRIPT FOR BOTH POSTGRESQL & SQL SERVER
# ---------------------------------------------------------
pg_sql_content = """-- ========================================================
-- POSTGRESQL SCHEMA & ANALYTICAL VIEWS
-- Project: E-Commerce & Customer Intelligence Analytics
-- ========================================================

DROP TABLE IF EXISTS fact_order_items CASCADE;
DROP TABLE IF EXISTS fact_orders CASCADE;
DROP TABLE IF EXISTS dim_products CASCADE;
DROP TABLE IF EXISTS dim_customers CASCADE;

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
    unit_cost NUMERIC(10,2),
    unit_price NUMERIC(10,2)
);

CREATE TABLE fact_orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES dim_customers(customer_id),
    order_date DATE,
    shipping_date DATE,
    shipping_cost NUMERIC(10,2),
    payment_method VARCHAR(30),
    order_status VARCHAR(20)
);

CREATE TABLE fact_order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES fact_orders(order_id),
    product_id INT REFERENCES dim_products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    discount_amount NUMERIC(10,2),
    net_revenue NUMERIC(10,2)
);

-- Copy commands (run in psql or pgAdmin query tool, updating absolute paths):
-- \\copy dim_customers FROM 'data/dim_customers.csv' WITH (FORMAT csv, HEADER true);
-- \\copy dim_products FROM 'data/dim_products.csv' WITH (FORMAT csv, HEADER true);
-- \\copy fact_orders FROM 'data/fact_orders.csv' WITH (FORMAT csv, HEADER true);
-- \\copy fact_order_items FROM 'data/fact_order_items.csv' WITH (FORMAT csv, HEADER true);

-- ---------------------------------------------------------
-- VIEW 1: RFM Customer Segmentation
-- ---------------------------------------------------------
CREATE OR REPLACE VIEW vw_customer_rfm AS
WITH customer_aggregates AS (
    SELECT 
        o.customer_id,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.net_revenue) AS monetary_value,
        ((SELECT MAX(order_date) FROM fact_orders) - MAX(o.order_date)) AS recency_days
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

-- ---------------------------------------------------------
-- VIEW 2: Monthly Cohort Retention Matrix
-- ---------------------------------------------------------
CREATE OR REPLACE VIEW vw_cohort_retention AS
WITH customer_first_order AS (
    SELECT 
        customer_id,
        DATE_TRUNC('month', MIN(order_date))::DATE AS cohort_month
    FROM fact_orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),
customer_monthly_activity AS (
    SELECT DISTINCT
        o.customer_id,
        DATE_TRUNC('month', o.order_date)::DATE AS activity_month
    FROM fact_orders o
    WHERE o.order_status = 'Completed'
),
cohort_progression AS (
    SELECT 
        cfo.cohort_month,
        cma.activity_month,
        (EXTRACT(YEAR FROM cma.activity_month) - EXTRACT(YEAR FROM cfo.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM cma.activity_month) - EXTRACT(MONTH FROM cfo.cohort_month)) AS cohort_index,
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
    ROUND((cp.active_customers::NUMERIC / cs.total_cohort_size) * 100, 2) AS retention_rate_pct
FROM cohort_progression cp
JOIN cohort_sizes cs ON cp.cohort_month = cs.cohort_month
ORDER BY cp.cohort_month, cp.cohort_index;
"""

with open(os.path.join(SQL_DIR, "postgres_setup.sql"), "w", encoding="utf-8") as f:
    f.write(pg_sql_content)

# SQL Server setup
sqlserver_content = """-- ========================================================
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

-- BULK INSERT dim_customers FROM 'C:\\...\\dim_customers.csv' WITH (FIRSTROW = 2, FIELDTERMINATOR = ',', ROWTERMINATOR = '\\n');
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
"""

with open(os.path.join(SQL_DIR, "sqlserver_setup.sql"), "w", encoding="utf-8") as f:
    f.write(sqlserver_content)

print("Generated SQL scripts for both PostgreSQL and SQL Server successfully!")
