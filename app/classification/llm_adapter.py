# app/classification/llm_adapter.py
from typing import Dict, Any
from app.classification.sklearn_model import SklearnClassifier

class LLMAdapter:
    """
    Optional LLM-assisted classification using MCP context.
    For HF Spaces or local experiments.
    """
    def __init__(self):
        self.baseline = SklearnClassifier()

    def predict(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # call baseline classifier
        result = self.baseline.predict(text)
        # ensure always valid
        if result["label"] not in ["finance.invoice", "hr.policy", "legal.contract"]:
            result["label"] = "finance.invoice"
        # optionally adjust confidence
        if context and context.get("policies_applied"):
            result["confidence"] = min(result["confidence"] + 0.1, 0.99)
        return result
