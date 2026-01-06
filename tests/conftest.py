import sys
from pathlib import Path

# Ensure root folder is in Python path so `import app` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from app.orchestration.mcp_client import start_embedded_mcp_servers, stop_embedded_mcp_servers

@pytest.fixture(scope="session", autouse=True)
def embedded_mcp_servers():
    """
    Starts embedded MCP servers for all tests that require MCP context.
    Runs once per test session.
    """
    start_embedded_mcp_servers()
    yield
    stop_embedded_mcp_servers()
