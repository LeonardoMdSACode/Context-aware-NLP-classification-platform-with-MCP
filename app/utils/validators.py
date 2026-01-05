from typing import Dict, Any, List


def validate_metadata(metadata: Dict[str, Any], required_keys: List[str] = None) -> bool:
    """
    Ensures metadata contains all required keys.
    """
    if not metadata:
        return not required_keys  # valid if no required keys

    if required_keys:
        missing = [k for k in required_keys if k not in metadata]
        if missing:
            raise ValueError(f"Missing required metadata keys: {missing}")

    return True


def validate_context(context: Any) -> bool:
    """
    Ensures MCP context is well-formed.
    Expects an object with:
    - taxonomy: dict
    - policies: dict
    - history: dict
    - sources: list
    """
    if not hasattr(context, "taxonomy") or not isinstance(context.taxonomy, dict):
        raise TypeError("Context missing 'taxonomy' dict")
    if not hasattr(context, "policies") or not isinstance(context.policies, dict):
        raise TypeError("Context missing 'policies' dict")
    if not hasattr(context, "history") or not isinstance(context.history, dict):
        raise TypeError("Context missing 'history' dict")
    if not hasattr(context, "sources") or not isinstance(context.sources, list):
        raise TypeError("Context missing 'sources' list")

    return True
