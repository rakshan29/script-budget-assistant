import os
from dotenv import load_dotenv
import clickhouse_connect

load_dotenv()
host=os.environ.get("CLICKHOUSE_HOST")
print(f"Connecting to host: {host}")

ch_client = clickhouse_connect.get_client(
    host=os.environ.get("CLICKHOUSE_HOST"),
    port=int(os.environ.get("CLICKHOUSE_PORT", 8443)),
    username=os.environ.get("CLICKHOUSE_USER", "default"),
    password=os.environ.get("CLICKHOUSE_PASSWORD"),
    database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
    secure=True,
)

# Query using the exact column names in your schema
result = ch_client.query(
    "SELECT category, department, description, estimated_cost FROM budget_items"
)

print("\n📊 Saved Budget Items in ClickHouse Cloud:")
print("-" * 60)
for row in result.result_rows:
    print(
        f"Category: {row[0]} | Dept: {row[1]} | Desc: {row[2]} | Cost: ${row[3]:,.2f}"
    )
