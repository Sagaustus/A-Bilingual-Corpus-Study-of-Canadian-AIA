"""Database connection and cached query runner for the AIA Corpus Dashboard."""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

DSN = "dbname=aia_corpus user=augustinefarinola host=localhost port=5432"


def get_connection():
    """Return a psycopg2 connection (cached per Streamlit session)."""
    return psycopg2.connect(DSN)


@st.cache_data(ttl=600)
def run_query(sql: str) -> pd.DataFrame:
    """Execute SQL and return a DataFrame. Results cached for 10 minutes."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df


def sql_expander(label: str, sql: str):
    """Show the raw SQL query in a collapsible expander for traceability."""
    with st.expander(f"View SQL — {label}"):
        st.code(sql.strip(), language="sql")
