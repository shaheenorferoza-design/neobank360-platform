from fastapi import FastAPI
from pydantic import BaseModel
import snowflake.connector

# =========================
# FastAPI App
# =========================

app = FastAPI()

# =========================
# Snowflake Connection
# =========================

conn = snowflake.connector.connect(
    user='FEROZAFLAKE2026',
    password='Llkkjjhh8877^^',
    account='WFKJRHG-LN75957',
    warehouse='NEOBANK_WH',
    database='NEOBANK360',
    schema='RAW',
    role='ACCOUNTADMIN'
)

# =========================
# Transaction Model
# =========================

class Transaction(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    transaction_type: str


# =========================
# Customer Model
# =========================

class Customer(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    city: str


# =========================
# Account Model
# =========================

class Account(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    status: str


# =========================
# Transaction API
# =========================

@app.post("/transactions")
def load_transaction(data: Transaction):

    cur = conn.cursor()

    insert_query = f"""
    INSERT INTO RAW.TRANSACTIONS
    (
        TRANSACTION_ID,
        CUSTOMER_ID,
        AMOUNT,
        TRANSACTION_TYPE,
        LOAD_TS
    )
    VALUES
    (
        '{data.transaction_id}',
        '{data.customer_id}',
        {data.amount},
        '{data.transaction_type}',
        CURRENT_TIMESTAMP()
    )
    """

    cur.execute(insert_query)

    return {
        "status": "success",
        "message": "Transaction Loaded"
    }


# =========================
# Customer API
# =========================

@app.post("/customers")
def load_customer(data: Customer):

    cur = conn.cursor()

    insert_query = f"""
    INSERT INTO RAW.CUSTOMERS
    (
        CUSTOMER_ID,
        FIRST_NAME,
        LAST_NAME,
        EMAIL,
        PHONE,
        CITY,
        CREATED_TS
    )
    VALUES
    (
        '{data.customer_id}',
        '{data.first_name}',
        '{data.last_name}',
        '{data.email}',
        '{data.phone}',
        '{data.city}',
        CURRENT_TIMESTAMP()
    )
    """

    cur.execute(insert_query)

    return {
        "status": "success",
        "message": "Customer Loaded"
    }


# =========================
# Account API
# =========================

@app.post("/accounts")
def load_account(data: Account):

    cur = conn.cursor()

    insert_query = f"""
    INSERT INTO RAW.ACCOUNTS
    (
        ACCOUNT_ID,
        CUSTOMER_ID,
        ACCOUNT_TYPE,
        BALANCE,
        STATUS,
        CREATED_TS
    )
    VALUES
    (
        '{data.account_id}',
        '{data.customer_id}',
        '{data.account_type}',
        {data.balance},
        '{data.status}',
        CURRENT_TIMESTAMP()
    )
    """

    cur.execute(insert_query)

    return {
        "status": "success",
        "message": "Account Loaded"
    }