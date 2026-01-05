from typing import Dict
from app.classification.preprocess import clean_text
import random

class SklearnClassifier:
    """
    Placeholder baseline classifier.

    - Replace with trained scikit-learn model or lightweight transformer.
    - Deterministic for testing / example purposes.
    """

    def __init__(self):
        # Load pre-trained model here in production
        self.labels = ["finance.invoice", "hr.policy", "legal.contract"]

    def predict(self, text: str) -> Dict[str, float]:
        text = clean_text(text)
        # deterministic mock confidence
        confidence = round(random.uniform(0.6, 0.95), 2)
        label = self.labels[hash(text) % len(self.labels)]
        return {"label": label, "confidence": confidence}
