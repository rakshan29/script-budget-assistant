import os
import uuid
import clickhouse_connect
from agent_pipeline import parse_script_to_budget
from dotenv import load_dotenv
load_dotenv()

def process_script_and_update_db(script_text: str):
    """
    Processes the screenplay excerpt with Gemini tool calls and handles the result response cleanly.
    """
    try:
        # Executes Gemini agent pipeline (tool calls perform ClickHouse inserts directly)
        response = parse_script_to_budget(script_text)

        # Extract structured text summary if available
        summary_text = getattr(
            response, "text", "Script processed successfully via Gemini tool calls."
        )

        return {"status": "success", "message": summary_text, "raw_response": response}
    except Exception as e:
        print(f"Error processing script in runner: {e}")
        return {"status": "error", "message": str(e)}
