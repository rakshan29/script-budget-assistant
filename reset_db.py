import os
import clickhouse_connect


def reset_table():
    client = clickhouse_connect.get_client(
        host=os.environ.get("CLICKHOUSE_HOST"),
        port=int(os.environ.get("CLICKHOUSE_PORT", 8443)),
        username=os.environ.get("CLICKHOUSE_USER", "default"),
        password=os.environ.get("CLICKHOUSE_PASSWORD"),
        database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
        secure=True,
    )

    print("Dropping old table if it exists...")
    client.command("DROP TABLE IF EXISTS budget_items")

    print("Creating budget_items table with matching schema...")
    create_table_query = """
    CREATE TABLE budget_items (
        category String,
        description String,
        estimated_cost Float64,
        department String,
        created_at DateTime DEFAULT now()
    ) ENGINE = MergeTree()
    ORDER BY (department, category)
    """
    client.command(create_table_query)
    print("✅ Table 'budget_items' successfully recreated!")


if __name__ == "__main__":
    reset_table()
