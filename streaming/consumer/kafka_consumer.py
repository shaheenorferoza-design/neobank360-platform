import json
from kafka import KafkaConsumer
import snowflake.connector

consumer = KafkaConsumer(
    'banking_transactions',
    bootstrap_servers='127.0.0.1:19092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

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

print("Kafka Consumer started...")

for message in consumer:

    payload = message.value

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
            f"kafka_offset_{message.offset}",
            json.dumps(payload)
        )
    )

    conn.commit()

    print(f"Loaded event: {payload['event_id']}")