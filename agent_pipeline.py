import os
import json
import clickhouse_connect
from google import genai
from google.genai import types
from logger import log_tool_execution, logger
from dotenv import load_dotenv

load_dotenv()

# Initialize ClickHouse Client
ch_client = clickhouse_connect.get_client(
    host=os.environ.get("CLICKHOUSE_HOST"),
    port=int(os.environ.get("CLICKHOUSE_PORT", 8443)),
    username=os.environ.get("CLICKHOUSE_USER", "default"),
    password=os.environ.get("CLICKHOUSE_PASSWORD"),
    database=os.environ.get("CLICKHOUSE_DATABASE", "default"),
    secure=True,
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def register_budget_line_item(
    category: str, description: str, estimated_cost: float, department: str
) -> str:
    """Registers a parsed line-item budget entry into ClickHouse."""
    logger.info(f"Registering budget line item: {description} under {department}")

    query = """
        INSERT INTO budget_items (category, description, estimated_cost, department, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """
    ch_client.command(query, [category, description, estimated_cost, department])

    return f"Successfully logged budget item: {description} (${estimated_cost}) under {department}."


available_tools = {"register_budget_line_item": register_budget_line_item}


def run_budget_agent(script_excerpt: str):
    system_instruction = (
        "You are an expert Line Producer and Film Budget Agent. "
        "Analyze the provided movie script segment, identify distinct production resource requirements, "
        "and ALWAYS call the 'register_budget_line_item' tool for EVERY identified item."
    )

    print("\n🚀 [STARTING AGENT] Sending script excerpt to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=script_excerpt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[register_budget_line_item],
            temperature=0.1,
        ),
    )

    if response.function_calls:
        print(
            f"⚙️ [TOOL CALL DETECTED] Gemini invoked {len(response.function_calls)} tool(s)."
        )
        for function_call in response.function_calls:
            name = function_call.name
            args = function_call.args

            if name in available_tools:
                tool_result = log_tool_execution(name, args, available_tools[name])
                print(f"✅ [TOOL EXECUTED]: {tool_result}")
            else:
                print(f"❌ Error: Tool {name} not found.")
    elif response.text:
        print("📝 [MODEL RESPONSE]:")
        print(response.text)


def parse_script_to_budget(script_excerpt: str):
    """Parses a script segment using Gemini and executes budget tool calls."""
    system_instruction = (
        "You are an expert Line Producer and Film Budget Agent. "
        "Analyze the provided movie script segment, identify distinct production resource requirements, "
        "and ALWAYS call the 'register_budget_line_item' tool for EVERY identified item."
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=script_excerpt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[register_budget_line_item],
            temperature=0.1,
        ),
    )

    if response.function_calls:
        for function_call in response.function_calls:
            name = function_call.name
            args = function_call.args
            if name in available_tools:
                log_tool_execution(name, args, available_tools[name])

    return response


# Alias in case run_budget_agent was referenced elsewhere
run_budget_agent = parse_script_to_budget
if __name__ == "__main__":
    sample_script = """
    EXT. NEO-TOKYO STREETS - NIGHT (SCENE 101)
    Heavy synthetic rain pours over glowing billboards.

    INT. SUB-LEVEL 'B' - CONTINUOUS
    VFX sequence: Holographic explosion featuring ~1,000 entity particles.
    Category: VFX
    Department: Visual Effects
    Cost: 125000.75
    """
    run_budget_agent(sample_script)
