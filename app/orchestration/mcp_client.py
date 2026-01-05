import subprocess
import atexit
import time
from typing import Any, Dict, Optional
import requests

from app.config import get_settings

settings = get_settings()

# -------------------------
# Embedded MCP Servers
# -------------------------
_embedded_processes: Dict[str, subprocess.Popen] = {}


def start_embedded_mcp_servers() -> None:
    """
    Start MCP servers in-process (subprocess) for HF Spaces / single-container deployments.
    """
    global _embedded_processes

    # Prevent duplicate starts
    if _embedded_processes:
        return

    servers = {
        "taxonomy": f"{settings.BASE_DIR}/mcp_servers/taxonomy_server/server.py",
        "policy": f"{settings.BASE_DIR}/mcp_servers/policy_server/server.py",
        "history": f"{settings.BASE_DIR}/mcp_servers/history_server/server.py",
    }

    for name, path in servers.items():
        proc = subprocess.Popen(
            ["python", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _embedded_processes[name] = proc

    # Ensure cleanup on exit
    atexit.register(stop_embedded_mcp_servers)

    # Wait a short time for servers to start
    time.sleep(2)


def stop_embedded_mcp_servers() -> None:
    """
    Stop any running embedded MCP servers.
    """
    global _embedded_processes
    for proc in _embedded_processes.values():
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
    _embedded_processes = {}


# -------------------------
# MCP Fetch Utilities
# -------------------------
def _fetch_mcp(url: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Helper to fetch structured context from an MCP endpoint.
    """
    try:
        resp = requests.post(url, json=payload or {}, timeout=settings.MCP_TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


def fetch_taxonomy_context(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Query taxonomy MCP server.
    """
    if settings.MCP_EMBEDDED:
        url = "http://localhost:7001/resolve"
    else:
        url = settings.MCP_TAXONOMY_URL + "/resolve"

    payload = {"text": text, "metadata": metadata}
    return _fetch_mcp(url, payload)


def fetch_policy_context(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Query policy MCP server.
    """
    if settings.MCP_EMBEDDED:
        url = "http://localhost:7002/resolve"
    else:
        url = settings.MCP_POLICY_URL + "/resolve"

    payload = {"text": text, "metadata": metadata}
    return _fetch_mcp(url, payload)


def fetch_history_context(text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Query historical labels MCP server.
    """
    if settings.MCP_EMBEDDED:
        url = "http://localhost:7003/resolve"
    else:
        url = settings.MCP_HISTORY_URL + "/resolve"

    payload = {"text": text, "metadata": metadata}
    return _fetch_mcp(url, payload)
