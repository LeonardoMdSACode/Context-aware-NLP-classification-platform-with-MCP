import json
from pathlib import Path
from datetime import datetime
from app.config import get_settings

settings = get_settings()

LOG_FILE = settings.LOG_DIR / "inference.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log_inference(
    label: str,
    confidence: float,
    abstained: bool,
    text: str,
    context: dict = None,
    metadata: dict = None,
) -> None:
    """
    Logs full classification inference results.
    Each log entry is JSON-serialized for reproducibility and debugging.
    """
    if not settings.LOG_INFERENCE:
        return

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "text_sample": text[:100],
        "metadata": metadata or {},
        "label": label,
        "confidence": confidence,
        "abstained": abstained,
        "context_summary": context.summary() if hasattr(context, "summary") else context,
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
