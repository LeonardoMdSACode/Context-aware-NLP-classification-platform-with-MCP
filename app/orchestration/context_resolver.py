from typing import Any, Dict, List, Optional

from app.config import get_settings
from app.orchestration.mcp_client import (
    fetch_taxonomy_context,
    fetch_policy_context,
    fetch_history_context,
)


class ResolvedContext:
    """
    Immutable container for resolved MCP context.
    """

    def __init__(
        self,
        taxonomy: Optional[Dict[str, Any]],
        policies: Optional[Dict[str, Any]],
        history: Optional[Dict[str, Any]],
        sources: List[str],
    ):
        self.taxonomy = taxonomy or {}
        self.policies = policies or {}
        self.history = history or {}
        self.sources = sources

    def to_dict(self) -> Dict[str, Any]:
        return {
            "taxonomy": self.taxonomy,
            "policies": self.policies,
            "history": self.history,
        }

    def summary(self) -> Dict[str, Any]:
        """
        Compact, audit-friendly summary of context usage.
        """
        return {
            "taxonomy_version": self.taxonomy.get("version"),
            "policies_applied": list(self.policies.keys()),
            "history_used": bool(self.history),
        }


def resolve_context(
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> ResolvedContext:
    """
    Resolve structured context via MCP.

    Rules:
    - Context is explicit and deterministic
    - Failures are isolated per source
    - No implicit retries or inference-time heuristics
    """

    settings = get_settings()
    sources_used: List[str] = []

    taxonomy_ctx = None
    policy_ctx = None
    history_ctx = None

    # -------------------------
    # Taxonomy Context
    # -------------------------
    try:
        taxonomy_ctx = fetch_taxonomy_context(text=text, metadata=metadata)
        if taxonomy_ctx:
            sources_used.append("taxonomy_server")
    except Exception:
        if settings.MCP_FAIL_FAST:
            raise

    # -------------------------
    # Policy Context
    # -------------------------
    try:
        policy_ctx = fetch_policy_context(text=text, metadata=metadata)
        if policy_ctx:
            sources_used.append("policy_server")
    except Exception:
        if settings.MCP_FAIL_FAST:
            raise

    # -------------------------
    # Historical Context
    # -------------------------
    try:
        history_ctx = fetch_history_context(text=text, metadata=metadata)
        if history_ctx:
            sources_used.append("history_server")
    except Exception:
        if settings.MCP_FAIL_FAST:
            raise

    return ResolvedContext(
        taxonomy=taxonomy_ctx,
        policies=policy_ctx,
        history=history_ctx,
        sources=sources_used,
    )
