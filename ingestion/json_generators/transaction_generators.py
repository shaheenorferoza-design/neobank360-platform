"""Transaction streaming generator."""

import random
import time
import uuid
import requests

transaction_types = ["DEBIT", "CREDIT"]

while True:

    payload = {
        
        "transaction_id": f"TXN_{uuid.uuid4().hex[:8]}",
        "customer_id": f"CUST{random.randint(1000, 9999)}",
        "amount": round(random.uniform(100, 10000), 2),
        "transaction_type": random.choice(transaction_types)
    }

    response = requests.post(
        "http://127.0.0.1:8000/transactions",
        json=payload,
        timeout=10
    )

    print("Transaction Sent:", payload)
    print("Response:", response.json())

    time.sleep(3)