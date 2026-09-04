import os
import clickhouse_connect
from dotenv import load_dotenv
load_dotenv()

def get_client():
    """Connects to ClickHouse Cloud using Replit Secrets."""
    return clickhouse_connect.get_client(
        host=os.environ.get("CLICKHOUSE_HOST"),
        port=int(os.environ.get("CLICKHOUSE_PORT", 8443)),
        username=os.environ.get("CLICKHOUSE_USER", "default"),
        password=os.environ.get("CLICKHOUSE_PASSWORD"),
        database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
        secure=True,
    )


get_clickhouse_client = get_client


def get_budget_by_category():
    """Fetches total budget costs aggregated by category."""
    try:
        client = get_client()
        query = "SELECT category, SUM(estimated_cost) as total_cost FROM budget_items GROUP BY category ORDER BY total_cost DESC"
        result = client.query(query)
        return [
            {"category": row[0], "total_cost": float(row[1])}
            for row in result.result_rows
        ]
    except Exception as e:
        print(f"Error fetching category budget: {e}")
        return []


def get_budget_by_scene():
    """Fetches total budget costs aggregated per department."""
    try:
        client = get_client()
        query = "SELECT department, SUM(estimated_cost) as total_cost FROM budget_items GROUP BY department ORDER BY total_cost DESC"
        result = client.query(query)
        return [
            {"department": str(row[0]), "total_cost": float(row[1])}
            for row in result.result_rows
        ]
    except Exception as e:
        print(f"Error fetching scene/department budget: {e}")
        return []


def get_total_budget_summary():
    """Fetches overall budget totals, department counts, and line item counts."""
    try:
        client = get_client()
        query = """
        SELECT 
            SUM(estimated_cost) as total_cost,
            uniqExact(department) as total_scenes,
            count() as total_items
        FROM budget_items
        """
        result = client.query(query)
        if result.result_rows and result.result_rows[0][0] is not None:
            row = result.result_rows[0]
            return {
                "total_cost": float(row[0]),
                "total_scenes": int(row[1]),
                "total_items": int(row[2]),
            }
        return {"total_cost": 0.0, "total_scenes": 0, "total_items": 0}
    except Exception as e:
        print(f"Error fetching summary: {e}")
        return {"total_cost": 0.0, "total_scenes": 0, "total_items": 0}


def get_all_line_items():
    """Fetches all itemized line items stored in ClickHouse."""
    try:
        client = get_client()
        query = (
            "SELECT category, department, description, estimated_cost FROM budget_items"
        )
        result = client.query(query)
        return [
            {
                "category": row[0],
                "department": row[1],
                "description": row[2],
                "cost": float(row[3]),
            }
            for row in result.result_rows
        ]
    except Exception as e:
        print(f"Error fetching line items: {e}")
        return []


get_total_budget = get_total_budget_summary
get_all_budget_items = get_all_line_items
clear_budget_data = lambda: get_client().command(
    "TRUNCATE TABLE IF EXISTS budget_items"
)
