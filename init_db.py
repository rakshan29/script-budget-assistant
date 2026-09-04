import os
import clickhouse_connect

def init_database():
    print("Connecting to ClickHouse Cloud...")

    client = clickhouse_connect.get_client(
        host=os.environ.get('CLICKHOUSE_HOST'),
        port=int(os.environ.get('CLICKHOUSE_PORT', 8443)),
        username=os.environ.get('CLICKHOUSE_USER', 'default'),
        password=os.environ.get('CLICKHOUSE_PASSWORD'),
        database=os.environ.get('CLICKHOUSE_DATABASE', 'default'),
        secure=True
    )

    # 1. Table for Scene Breakdowns
    scenes_table_sql = """
    CREATE TABLE IF NOT EXISTS scenes (
        project_id String,
        scene_number UInt16,
        scene_heading String,
        location String,
        time_of_day String,
        summary String,
        created_at DateTime DEFAULT now()
    ) ENGINE = MergeTree()
    ORDER BY (project_id, scene_number);
    """

    # 2. Table for Budget Line Items
    budget_table_sql = """
    CREATE TABLE IF NOT EXISTS budget_items (
        project_id String,
        scene_number UInt16,
        category String,
        item_name String,
        unit_cost Float64,
        quantity UInt16,
        total_cost Float64,
        created_at DateTime DEFAULT now()
    ) ENGINE = MergeTree()
    ORDER BY (project_id, category, scene_number);
    """

    print("Creating table: scenes...")
    client.command(scenes_table_sql)

    print("Creating table: budget_items...")
    client.command(budget_table_sql)

    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()