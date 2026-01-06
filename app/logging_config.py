import logging
import sys
from pathlib import Path

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

def setup_logging():
    handlers = []

    # Always log to stdout (HF Spaces, Docker, CI)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    handlers.append(stdout_handler)

    # Optional file logging (local only)
    logs_dir = Path("logs")
    try:
        logs_dir.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(logs_dir / "app.log")
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        handlers.append(file_handler)
    except Exception:
        # Fail silently — file logs are non-critical
        pass

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=handlers,
        force=True,  # overrides uvicorn defaults
    )

    # Reduce noise from dependencies
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
