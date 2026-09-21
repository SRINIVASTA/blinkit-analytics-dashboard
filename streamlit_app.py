import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

# --- AUTOMATED DATABASE CHECK ---
# --- UPDATE THIS AT THE TOP OF streamlit_app.py ---
BASE_DIR = os.path.dirname(__file__) if "__file__" in locals() else "."
DB_PATH = os.path.join(BASE_DIR, "data", "blinkit.db")

# Force a clean overwrite if things are broken
if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) < 100:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH) # Delete the broken empty file
    st.info("Generating fresh mock tables on server...")
    try:
        import db_generator
        db_generator.generate_mock_data()
        st.success("Successfully generated blinkit.db!")
        st.rerun()
    except Exception as e:
        st.error(f"Generator Error: {e}")
# --------------------------------

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def run_query(sql):
    conn = get_db_connection()
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
