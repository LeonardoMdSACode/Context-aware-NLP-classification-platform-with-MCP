from typing import Any, Dict, Optional

from app.classification.sklearn_model import SklearnClassifier
from app.classification.llm_adapter import LLMAdapter
from app.config import get_settings

settings = get_settings()


class Classifier:
    """
    Abstract classifier. Can switch between:
    - Sklearn baseline
    - Optional LLM-assisted classification
    """

    def __init__(self):
        self.model = SklearnClassifier()
        self.llm = LLMAdapter() if settings.MCP_EMBEDDED else None

    def predict(
        self, text: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict label using structured context.
        Returns dict: {label, confidence}
        """

        # Step 1: baseline model
        baseline_result = self.model.predict(text)

        # Step 2: optionally re-rank / adjust using LLM + context
        if self.llm:
            llm_result = self.llm.predict(text=text, context=context)
            # Simple merge: prefer LLM if confidence > baseline
            if llm_result["confidence"] > baseline_result["confidence"]:
                return llm_result

        return baseline_result
