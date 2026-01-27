# app\orchestration\context_resolver.py
from typing import Any, Dict, List, Optional
from pathlib import Path
import json

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


def _load_local_json(path: str) -> Dict[str, Any]:
    """Safely load local JSON file, return empty dict if missing or invalid."""
    try:
        file_path = Path(path)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception:
        return {}


def resolve_context(
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> ResolvedContext:
    """
    Resolve structured context via MCP.

    - Uses local embedded JSON files if MCP_EMBEDDED=True
    - Otherwise uses fetch_* functions to retrieve context from distributed MCP servers
    """
    settings = get_settings()
    metadata = metadata or {}
    sources_used: List[str] = []

    taxonomy_ctx = None
    policy_ctx = None
    history_ctx = None

    if settings.MCP_EMBEDDED:
        # -------------------------
        # Load local JSONs
        # -------------------------
        taxonomy_ctx = _load_local_json(settings.MCP_TAXONOMY_URL)
        if taxonomy_ctx:
            sources_used.append(str(Path(settings.MCP_TAXONOMY_URL).name))

        policy_ctx = _load_local_json(settings.MCP_POLICY_URL)
        if policy_ctx:
            sources_used.append(str(Path(settings.MCP_POLICY_URL).name))

        history_ctx = _load_local_json(settings.MCP_HISTORY_URL)
        if history_ctx:
            sources_used.append(str(Path(settings.MCP_HISTORY_URL).name))

    else:
        # -------------------------
        # Distributed MCP
        # -------------------------
        try:
            taxonomy_ctx = fetch_taxonomy_context(text=text, metadata=metadata)
            if taxonomy_ctx:
                sources_used.append("taxonomy_server")
        except Exception:
            if settings.MCP_FAIL_FAST:
                raise

        try:
            policy_ctx = fetch_policy_context(text=text, metadata=metadata)
            if policy_ctx:
                sources_used.append("policy_server")
        except Exception:
            if settings.MCP_FAIL_FAST:
                raise

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
