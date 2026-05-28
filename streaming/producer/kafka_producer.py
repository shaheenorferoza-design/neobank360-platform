import json
import uuid
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:19092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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
        "event_id": str(uuid.uuid4()),
        "customer_id": f"C{random.randint(101,110)}",
        "account_id": f"A{random.randint(1001,1010)}",
        "event_type": random.choice(event_types),
        "amount": random.randint(100,50000),
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

    producer.send(
        'banking_transactions',
        value=event
    )

    print("Produced:", event["event_id"])

    time.sleep(3)