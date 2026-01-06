from typing import Any, Dict, Optional
from pathlib import Path

from app.classification.sklearn_model import SklearnClassifier
from app.classification.llm_adapter import LLMAdapter
from app.config import get_settings

settings = get_settings()


class Classifier:
    """
    Abstract classifier. Can switch between:
    - Sklearn baseline (trained from JSON dataset)
    - Optional LLM-assisted classification
    """

    def __init__(self, dataset_path: Optional[str] = None):
        # Use default training dataset if none provided
        default_dataset = Path("data/samples/training_data.json")
        if dataset_path is None and default_dataset.exists():
            dataset_path = str(default_dataset)

        self.model = SklearnClassifier(dataset_path=dataset_path)
        self.llm = LLMAdapter() if settings.MCP_EMBEDDED else None

    def predict(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
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
