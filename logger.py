import json
import logging
import time
from datetime import datetime


# Formatter to output logs as clean JSON lines in Replit terminal
class StructuredJsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_data"):
            log_obj["data"] = record.extra_data
        return json.dumps(log_obj)


def setup_logger():
    handler = logging.StreamHandler()
    handler.setFormatter(StructuredJsonFormatter())
    logger = logging.getLogger("ScriptToBudget")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if logger is already set up
    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = setup_logger()


def log_tool_execution(tool_name: str, args: dict, func):
    """Wraps tool execution with execution time and JSON structured logs."""
    start_time = time.time()
    logger.info(f"Executing tool: {tool_name}", extra={"extra_data": {"args": args}})
    try:
        result = func(**args)
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"Tool '{tool_name}' succeeded",
            extra={"extra_data": {"duration_ms": duration_ms, "status": "success"}},
        )
        return result
    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(
            f"Tool '{tool_name}' failed: {str(e)}",
            extra={"extra_data": {"duration_ms": duration_ms, "error": str(e)}},
        )
        raise e
