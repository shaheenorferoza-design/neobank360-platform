import streamlit as st
import pandas as pd
import snowflake.connector

st.set_page_config(
    page_title="Neobank360 Fraud Dashboard",
    layout="wide"
)

st.title("🚨 Neobank360 Real-Time Fraud Dashboard")

conn = snowflake.connector.connect(
    user="ferozaflake2026",
    password="Llkkjjhh8877^^",
    account="WFKJRHG-LN75957",
    warehouse="NEOBANK_WH",
    database="NEOBANK360",
    schema="DATAMART",
    role="ACCOUNTADMIN"
)

query = """
select
    event_id,
    customer_id,
    event_type,
    amount,
    fraud_risk_level,
    txn_ts
from fct_high_velocity_transactions
order by txn_ts desc
limit 50
"""

df = pd.read_sql(query, conn)

st.metric(
    "Total Fraud Alerts",
    len(df)
)

high_risk = df[df["FRAUD_RISK_LEVEL"] == "HIGH"]

st.metric(
    "High Risk Alerts",
    len(high_risk)
)

st.subheader("Recent Fraud Transactions")

st.dataframe(df)

st.subheader("Fraud By Customer")

customer_counts = (
    df.groupby("CUSTOMER_ID")
      .size()
      .reset_index(name="ALERT_COUNT")
)

st.bar_chart(
    customer_counts.set_index("CUSTOMER_ID")
)