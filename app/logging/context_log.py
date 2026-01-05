import json
from pathlib import Path
from datetime import datetime
from app.config import get_settings

settings = get_settings()

LOG_FILE = settings.LOG_DIR / "context_usage.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_context_resolution(context: dict, text: str, metadata: dict = None) -> None:
    """
    Logs which MCP context sources were used during inference.
    Each log entry is JSON-serialized for easy auditing.
    """
    if not settings.LOG_CONTEXT_USAGE:
        return

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "text_sample": text[:100],  # store first 100 chars for brevity
        "metadata": metadata or {},
        "context_summary": context.summary() if hasattr(context, "summary") else context,
        "sources": getattr(context, "sources", None),
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
