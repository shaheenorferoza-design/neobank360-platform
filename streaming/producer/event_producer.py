import json
import random
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
output_dir = BASE_DIR / "sample_events"
output_dir.mkdir(parents=True, exist_ok=True)

event_types = [
    "UPI_PAYMENT",
    "CARD_SWIPE",
    "ATM_WITHDRAWAL",
    "NETBANKING_TRANSFER"
]

cities = [
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Chennai"
]

merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato"
]

while True:

    event = {
        "event_id": f"EVT{random.randint(1000,9999)}",
        "customer_id": f"C{random.randint(101,110)}",
        "account_id": f"A{random.randint(1001,1010)}",
        "event_type": random.choice(event_types),
        "amount": random.randint(100, 50000),
        "currency": "INR",

        "merchant": {
            "name": random.choice(merchants),
            "category": "ECOMMERCE"
        },

        "device": {
            "device_id": f"D{random.randint(1,20)}",
            "ip_address": f"10.1.1.{random.randint(1,255)}",
            "location": random.choice(cities)
        },

        "txn_ts": datetime.now().isoformat()
    }

    filename = output_dir / f"event_{int(time.time())}.json"

    with open(filename, "w") as f:
        json.dump(event, f, indent=2)

    print(f"Generated: {filename}")

    time.sleep(5)