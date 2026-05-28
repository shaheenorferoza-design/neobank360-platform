"""Account streaming generator."""

import random
import time
import uuid
import requests

account_types = ["SAVINGS", "CURRENT", "SALARY"]
statuses = ["ACTIVE", "INACTIVE"]

while True:

    payload = {
    
        "account_id": f"ACC_{uuid.uuid4().hex[:8]}",
        "customer_id": f"CUST{random.randint(1000, 9999)}",
        "account_type": random.choice(account_types),
        "balance": round(random.uniform(1000, 500000), 2),
        "status": random.choice(statuses)
    }

    response = requests.post(
        "http://127.0.0.1:8000/accounts",
        json=payload,
        timeout=10
    )

    print("Account Sent:", payload)
    print("Response:", response.json())

    time.sleep(5)