import pandas as pd
import random
from datetime import datetime, timedelta

# Read customers file
customers_df = pd.read_csv("../output/customers.csv")

accounts = []

account_types = [
    "SAVINGS",
    "CURRENT",
    "SALARY"
]

account_status = [
    "ACTIVE",
    "DORMANT",
    "BLOCKED"
]

for index, row in customers_df.iterrows():

    # Each customer can have 1 to 3 accounts
    number_of_accounts = random.randint(1, 3)

    for acc in range(number_of_accounts):

        account = {
            "account_id": f"ACC{index+1:05}{acc+1}",
            "customer_id": row["customer_id"],
            "account_type": random.choice(account_types),
            "branch_code": f"BR{random.randint(100,999)}",
            "open_date": datetime.now().date() - timedelta(days=random.randint(30, 3000)),
            "balance": round(random.uniform(1000, 1000000), 2),
            "status": random.choice(account_status)
        }

        accounts.append(account)

accounts_df = pd.DataFrame(accounts)

accounts_df.to_csv(
    r"C:\Users\arsha\OneDrive\Desktop\SHAHEEN\neobank360-platform\ingestion\output\accounts.csv",
    index=False
)

print("accounts.csv generated successfully")