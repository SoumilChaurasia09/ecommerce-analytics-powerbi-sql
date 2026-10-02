import csv
import os

BASE_DIR = r"C:\Users\soumi\.gemini\antigravity\scratch\ecommerce_bi_project"
DATA_DIR = os.path.join(BASE_DIR, "data")
SQL_DIR = os.path.join(BASE_DIR, "sql")

def generate_inserts(flavor="postgres"):
    output_path = os.path.join(SQL_DIR, f"seed_data_{flavor}.sql")
    
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(f"-- Auto-generated seed data for {flavor.upper()}\n\n")
        
        # 1. Dim Products
        out.write("-- 1. SEED DIM_PRODUCTS\n")
        with open(os.path.join(DATA_DIR, "dim_products.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            chunk_size = 50
            for i in range(0, len(rows), chunk_size):
                chunk = rows[i:i+chunk_size]
                out.write("INSERT INTO dim_products (product_id, product_name, category, sub_category, unit_cost, unit_price) VALUES\n")
                vals = []
                for r in chunk:
                    name_esc = r['product_name'].replace("'", "''")
                    vals.append(f"  ({r['product_id']}, '{name_esc}', '{r['category']}', '{r['sub_category']}', {r['unit_cost']}, {r['unit_price']})")
                out.write(",\n".join(vals) + ";\n\n")
                
        # 2. Dim Customers
        out.write("-- 2. SEED DIM_CUSTOMERS\n")
        with open(os.path.join(DATA_DIR, "dim_customers.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            chunk_size = 100
            for i in range(0, len(rows), chunk_size):
                chunk = rows[i:i+chunk_size]
                out.write("INSERT INTO dim_customers (customer_id, customer_name, email, region, signup_date) VALUES\n")
                vals = []
                for r in chunk:
                    name_esc = r['customer_name'].replace("'", "''")
                    vals.append(f"  ({r['customer_id']}, '{name_esc}', '{r['email']}', '{r['region']}', '{r['signup_date']}')")
                out.write(",\n".join(vals) + ";\n\n")

        # 3. Fact Orders
        out.write("-- 3. SEED FACT_ORDERS\n")
        with open(os.path.join(DATA_DIR, "fact_orders.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            # SQL Server supports max 1000 rows in a single INSERT VALUES statement
            chunk_size = 500
            for i in range(0, len(rows), chunk_size):
                chunk = rows[i:i+chunk_size]
                out.write("INSERT INTO fact_orders (order_id, customer_id, order_date, shipping_date, shipping_cost, payment_method, order_status) VALUES\n")
                vals = []
                for r in chunk:
                    vals.append(f"  ({r['order_id']}, {r['customer_id']}, '{r['order_date']}', '{r['shipping_date']}', {r['shipping_cost']}, '{r['payment_method']}', '{r['order_status']}')")
                out.write(",\n".join(vals) + ";\n\n")

        # 4. Fact Order Items
        out.write("-- 4. SEED FACT_ORDER_ITEMS\n")
        with open(os.path.join(DATA_DIR, "fact_order_items.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            chunk_size = 500
            for i in range(0, len(rows), chunk_size):
                chunk = rows[i:i+chunk_size]
                out.write("INSERT INTO fact_order_items (order_item_id, order_id, product_id, quantity, unit_price, discount_amount, net_revenue) VALUES\n")
                vals = []
                for r in chunk:
                    vals.append(f"  ({r['order_item_id']}, {r['order_id']}, {r['product_id']}, {r['quantity']}, {r['unit_price']}, {r['discount_amount']}, {r['net_revenue']})")
                out.write(",\n".join(vals) + ";\n\n")

    print(f"Generated {output_path}")

generate_inserts("postgres")
generate_inserts("sqlserver")
