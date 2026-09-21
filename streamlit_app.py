import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# Helper to locate database accurately
def get_db_connection():
    base_dir = os.path.dirname(__file__) if "__file__" in locals() else "."
    db_path = os.path.join(base_dir, "data", "blinkit.db")
    return sqlite3.connect(db_path)

def run_query(sql):
    conn = get_db_connection()
    # Read raw SQL results straight into a Pandas DataFrame
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

@st.cache_data(ttl=600, show_spinner="Querying SQLite Orders...")
def load_orders():
    df = run_query("SELECT * FROM blinkit_orders;")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["order_total"] = pd.to_numeric(df["order_total"], errors="coerce")
    return df

@st.cache_data(ttl=600, show_spinner="Querying SQLite Deliveries...")
def load_delivery():
    df = run_query("SELECT * FROM blinkit_delivery_performance;")
    df["distance_km"] = pd.to_numeric(df["distance_km"], errors="coerce")
    df["delivery_time_minutes"] = pd.to_numeric(df["delivery_time_minutes"], errors="coerce")
    return df

# ... (Keep the rest of load_order_items, load_marketing, and visual rendering tabs unchanged)
