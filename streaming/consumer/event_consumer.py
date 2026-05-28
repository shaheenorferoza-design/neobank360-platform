import json
import time
from pathlib import Path
import snowflake.connector

BASE_DIR = Path(__file__).resolve().parent.parent
EVENT_DIR = BASE_DIR / "sample_events"
PROCESSED_DIR = BASE_DIR / "processed_events"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

conn = snowflake.connector.connect(
    user="ferozaflake2026",
    password="Llkkjjhh8877^^",
    account="WFKJRHG-LN75957",
    warehouse="NEOBANK_WH",
    database="NEOBANK360",
    schema="RAW",
    role="ACCOUNTADMIN"
)

cur = conn.cursor()

print("Consumer started...")

while True:
    files = list(EVENT_DIR.glob("*.json"))

    for file_path in files:
        with open(file_path, "r") as f:
            payload = json.load(f)

        insert_sql = """
        insert into raw_transaction_events
        (
            source_file_name,
            source_row_number,
            event_payload
        )
        select
            %s,
            1,
            parse_json(%s)
        """

        cur.execute(
            insert_sql,
            (
                file_path.name,
                json.dumps(payload)
            )
        )

        conn.commit()

        processed_path = PROCESSED_DIR / file_path.name
        file_path.rename(processed_path)

        print(f"Loaded and moved: {file_path.name}")

    time.sleep(5)