"""Customer streaming generator."""

import random
import time
import uuid

import requests

first_names = ["John", "David", "Sara", "Priya", "Aman"]
last_names = ["Smith", "Kumar", "Sharma", "Ali", "Reddy"]
cities = ["Hyderabad", "Mumbai", "Delhi", "Bangalore"]

while True:

  
    customer_id = f"CUST_{uuid.uuid4().hex[:8]}"

    payload = {
        "customer_id": customer_id,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "email": f"{customer_id.lower()}@test.com",
        "phone": str(random.randint(9000000000, 9999999999)),
        "city": random.choice(cities)
    }

    response = requests.post(
        "http://127.0.0.1:8000/customers",
        json=payload,
        timeout=10
    )

    print("Customer Sent:", payload)
    print("Response:", response.json())

    time.sleep(5)