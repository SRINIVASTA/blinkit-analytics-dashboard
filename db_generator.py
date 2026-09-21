import os
import sqlite3
import random
from datetime import datetime, timedelta

def generate_mock_data():
    # Create the data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Connect to SQLite database (creates file if missing)
    db_path = os.path.join("data", "blinkit.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. CREATE THE TABLES
    cursor.execute("DROP TABLE IF EXISTS blinkit_orders;")
    cursor.execute("""
        CREATE TABLE blinkit_orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date TEXT,
            promised_delivery_time TEXT,
            actual_delivery_time TEXT,
            delivery_status TEXT,
            order_total REAL,
            payment_method TEXT,
            delivery_partner_id TEXT,
            store_id TEXT
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS blinkit_delivery_performance;")
    cursor.execute("""
        CREATE TABLE blinkit_delivery_performance (
            order_id TEXT PRIMARY KEY,
            delivery_partner_id TEXT,
            promised_time TEXT,
            actual_time TEXT,
            delivery_time_minutes INTEGER,
            distance_km REAL,
            delivery_status TEXT,
            reasons_if_delayed TEXT
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS blinkit_order_items;")
    cursor.execute("""
        CREATE TABLE blinkit_order_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            total_price REAL
        );
    """)

    cursor.execute("DROP TABLE IF EXISTS blinkit_marketing_performance;")
    cursor.execute("""
        CREATE TABLE blinkit_marketing_performance (
            campaign_id TEXT PRIMARY KEY,
            campaign_name TEXT,
            date TEXT,
            target_audience TEXT,
            channel TEXT,
            impressions INTEGER,
            clicks INTEGER,
            conversions INTEGER,
            spend REAL,
            revenue_generated REAL,
            roas REAL
        );
    """)

    # Seed settings
    NUM_ROWS = 100
    start_date = datetime(2026, 9, 1)
    order_ids = [f"ORD{1000 + i}" for i in range(NUM_ROWS)]
    customer_ids = [f"CUST{random.randint(100, 500)}" for _ in range(50)]
    partner_ids = [f"PARTNER{random.randint(10, 30)}" for _ in range(15)]
    store_ids = [f"STORE{random.randint(1, 5)}" for _ in range(5)]
    product_ids = [f"PROD{random.randint(500, 600)}" for _ in range(30)]
    channels = ["Instagram Ads", "Google Search", "Facebook Video", "YouTube Shorts", "Direct SMS"]
    delay_reasons = ["Heavy Traffic", "Rain / Waterlogging", "Store Sourcing Delay", "Customer Unreachable", "Wrong Address Pin"]

    # 2. POPULATE THE TABLES (100 Rows each)
    for i in range(NUM_ROWS):
        o_date = start_date + timedelta(days=random.randint(0, 19), hours=random.randint(8, 22), minutes=random.randint(0, 59))
        promised_time = o_date + timedelta(minutes=15)
        status = random.choices(["On Time", "Delayed", "Cancelled"], weights=[0.75, 0.20, 0.05])[0]
        
        if status == "On Time":
            actual_time = o_date + timedelta(minutes=random.randint(8, 14))
            time_min = random.randint(8, 14)
        elif status == "Delayed":
            actual_time = o_date + timedelta(minutes=random.randint(16, 35))
            time_min = random.randint(16, 35)
        else:
            actual_time = None
            time_min = 0

        order_total = random.randint(150, 1450)
        o_id = order_ids[i]
        p_method = random.choice(["UPI", "Credit Card", "Cash on Delivery", "Net Banking"])
        p_id = random.choice(partner_ids)
        s_id = random.choice(store_ids)

        # Insert Order
        cursor.execute("""
            INSERT INTO blinkit_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (o_id, random.choice(customer_ids), o_date.strftime("%Y-%m-%d %H:%M:%S"),
              promised_time.strftime("%Y-%m-%d %H:%M:%S"), actual_time.strftime("%Y-%m-%d %H:%M:%S") if actual_time else None,
              status, order_total, p_method, p_id, s_id))

        # Insert Delivery
        cursor.execute("""
            INSERT INTO blinkit_delivery_performance VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (o_id, p_id, promised_time.strftime("%Y-%m-%d %H:%M:%S"),
              actual_time.strftime("%Y-%m-%d %H:%M:%S") if actual_time else None,
              time_min, round(random.uniform(0.5, 6.2), 2), status,
              random.choice(delay_reasons) if status == "Delayed" else ""))

        # Insert Order Item
        qty = random.randint(1, 4)
        u_price = random.choice([40, 60, 120, 250, 450])
        cursor.execute("""
            INSERT INTO blinkit_order_items (order_id, product_id, quantity, unit_price, total_price) 
            VALUES (?, ?, ?, ?, ?);
        """, (random.choice(order_ids), random.choice(product_ids), qty, u_price, qty * u_price))

        # Insert Marketing Campaign
        m_date = start_date + timedelta(days=random.randint(0, 19))
        impressions = random.randint(5000, 50000)
        clicks = int(impressions * random.uniform(0.02, 0.08))
        conversions = int(clicks * random.uniform(0.10, 0.25))
        spend = random.randint(1500, 12000)
        rev_gen = int(spend * random.uniform(1.2, 4.5))
        roas = round(rev_gen / spend, 2)

        cursor.execute("""
            INSERT INTO blinkit_marketing_performance VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (f"CAMP{2000 + i}", f"Blinkit Flash Sale #{random.randint(1, 10)}", m_date.strftime("%Y-%m-%d"),
              random.choice(["GenZ Foodies", "Working Parents", "Late Night Cravers", "Daily Essentials Buyers"]),
              random.choice(channels), impressions, clicks, conversions, spend, rev_gen, roas))

    conn.commit()
    conn.close()
    print("✅ Success: Created 'data/blinkit.db' containing 4 relational SQL tables with 100 rows each!")

# This makes it execute automatically if you run it directly
if __name__ == "__main__":
    generate_mock_data()
