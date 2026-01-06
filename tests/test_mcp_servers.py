from app.orchestration.context_resolver import resolve_context
from app.config import get_settings

def test_mcp_fail_fast_disabled(embedded_mcp_servers):
    settings = get_settings()
    settings.MCP_FAIL_FAST = False

    # This should never raise, even if MCP endpoints are unreachable
    context = resolve_context(
        text="Invoice test",
        metadata={}
    )

    assert context is not None
    assert hasattr(context, "sources")
