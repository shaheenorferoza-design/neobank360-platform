import os
import json
import snowflake.connector
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

conn = snowflake.connector.connect(
    user="YOUR_USER",
    password="YOUR_PASSWORD",
    account="YOUR_ACCOUNT",
    warehouse="NEOBANK_WH",
    database="NEOBANK360",
    schema="DATAMART",
    role="ACCOUNTADMIN"
)

cur = conn.cursor()

cur.execute("""
select
    event_id,
    customer_id,
    fraud_risk_level,
    rule_triggered,
    genai_explanation,
    recommended_action
from datamart.fraud_alert_explanations
where event_id not in (
    select event_id
    from datamart.fraud_llm_explanations
)
limit 5
""")

rows = cur.fetchall()

for row in rows:
    event_id, customer_id, risk_level, rule_triggered, base_explanation, action = row

    prompt = f"""
You are a banking fraud analyst.

Explain this fraud alert in clear business language.

Customer ID: {customer_id}
Risk Level: {risk_level}
Rule Triggered: {rule_triggered}
System Explanation: {base_explanation}
Current Recommended Action: {action}

Return JSON with:
- explanation
- recommended_action
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise banking fraud risk analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
        llm_explanation = parsed.get("explanation", content)
        recommended_action = parsed.get("recommended_action", action)
    except Exception:
        llm_explanation = content
        recommended_action = action

    cur.execute(
        """
        insert into datamart.fraud_llm_explanations
        (
            event_id,
            customer_id,
            fraud_risk_level,
            llm_explanation,
            recommended_action,
            created_ts
        )
        values (%s, %s, %s, %s, %s, current_timestamp())
        """,
        (
            event_id,
            customer_id,
            risk_level,
            llm_explanation,
            recommended_action
        )
    )

conn.commit()

cur.close()
conn.close()

print(f"Generated LLM explanations for {len(rows)} fraud alerts.")