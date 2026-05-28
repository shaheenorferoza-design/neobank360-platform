from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker("en_IN")

customers = []

for i in range(1000):

    customer = {
        "customer_id": f"CUST{i+1:05}",
        "full_name": fake.name(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=75),
        "city": fake.city(),
        "state": fake.state(),
        "occupation": random.choice([
            "Engineer",
            "Doctor",
            "Teacher",
            "Business",
            "Lawyer",
            "Government Employee"
        ]),
        "kyc_status": random.choice([
            "VERIFIED",
            "PENDING",
            "REJECTED"
        ]),
        "risk_category": random.choice([
            "LOW",
            "MEDIUM",
            "HIGH"
        ]),
        "created_timestamp": datetime.now()
    }

    customers.append(customer)

df = pd.DataFrame(customers)

df.to_csv(r"C:\Users\arsha\OneDrive\Desktop\SHAHEEN\neobank360-platform\ingestion\output\customers.csv",
    index=False
)

print("customers.csv generated successfully")