import pandas as pd
import random
from datetime import datetime, timedelta

# Read accounts file
accounts_df = pd.read_csv(r"C:\Users\arsha\OneDrive\Desktop\SHAHEEN\neobank360-platform\ingestion\output\accounts.csv")

transactions = []

transaction_types = [
    "UPI",
    "ATM",
    "NEFT",
    "IMPS",
    "POS",
    "CASH_DEPOSIT"
]

transaction_status = [
    "SUCCESS",
    "FAILED",
    "PENDING"
]

merchant_names = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Reliance Mart",
    "Myntra",
    "Uber",
    "IRCTC"
]

for index, row in accounts_df.iterrows():

    # Each account gets random transactions
    number_of_transactions = random.randint(10, 50)

    for txn in range(number_of_transactions):

        amount = round(random.uniform(100, 50000), 2)

        # Fraud simulation
        fraud_flag = "NO"

        if amount > 40000:
            fraud_flag = "YES"

        transaction = {
            "transaction_id": f"TXN{index+1:05}{txn+1}",
            "account_id": row["account_id"],
            "transaction_timestamp": datetime.now() - timedelta(
                minutes=random.randint(1, 500000)
            ),
            "transaction_type": random.choice(transaction_types),
            "amount": amount,
            "merchant_name": random.choice(merchant_names),
            "payment_channel": random.choice([
                "MOBILE",
                "ATM",
                "WEB",
                "BRANCH"
            ]),
            "device_id": f"DEV{random.randint(10000,99999)}",
            "transaction_status": random.choice(transaction_status),
            "fraud_flag": fraud_flag
        }

        transactions.append(transaction)

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    r"C:\Users\arsha\OneDrive\Desktop\SHAHEEN\neobank360-platform\ingestion\output\transactions.csv",
    index=False
)

print("transactions.csv generated successfully")