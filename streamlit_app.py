import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# --- AUTOMATED DATABASE CHECK ---
BASE_DIR = os.path.dirname(__file__) if "__file__" in locals() else "."
DB_PATH = os.path.join(BASE_DIR, "data", "blinkit.db")

if not os.path.exists(DB_PATH):
    st.info("Database file not found. Generating fresh mock tables on server...")
    try:
        import db_generator
        st.success("Successfully generated blinkit.db with 100 rows!")
    except Exception as e:
        st.error(f"Failed to auto-generate mock database: {e}")
# --------------------------------

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def run_query(sql):
    conn = get_db_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
