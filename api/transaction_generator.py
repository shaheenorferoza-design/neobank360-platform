
"""Transaction streaming generator."""

import requests
import random
import time

transaction_types = ["DEBIT", "CREDIT"]

while True:

    payload = {
        "transaction_id": f"TXN{random.randint(1000, 9999)}",
        "customer_id": f"CUST{random.randint(100, 999)}",
        "amount": round(random.uniform(100, 10000), 2),
        "transaction_type": random.choice(transaction_types)
    }

    response = requests.post(
        "http://127.0.0.1:8000/transactions",
        json=payload,
        timeout=10
    )

    print("Sent:", payload)
    print("Response:", response.json())

    time.sleep(5)
