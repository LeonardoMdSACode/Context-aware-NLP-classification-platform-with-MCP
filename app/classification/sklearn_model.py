from typing import Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re
import json
from pathlib import Path
import joblib  # new import for saving/loading models

# Import from the module if already exists; else fallback to local definition
try:
    from app.classification.preprocess import clean_text as external_clean_text
    clean_text = external_clean_text
except ImportError:
    # -------------------------
    # Minimal preprocessing
    # -------------------------
    def clean_text(text: str) -> str:
        # Lowercase, remove extra spaces, standardize numeric patterns
        text = text.lower()
        text = re.sub(r"\d+", "NUM", text)  # Replace numbers with placeholder
        text = re.sub(r"\s+", " ", text)
        return text.strip()


class SklearnClassifier:
    """
    Lightweight TF-IDF + Logistic Regression classifier for finance/hr/legal.
    Deterministic and trainable from JSON dataset.
    """

    MODEL_PATH = Path(__file__).parent.parent / "models" / "trained_pipeline.joblib"

    def __init__(self, dataset_path: str = "data/samples/training_data.json"):
        """
        dataset_path: optional path to JSON file with training data
        format: [{"text": "...", "label": "finance.invoice"}, ...]
        """
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=500))
        ])
        self.is_trained = False

        # -------------------------
        # Load trained model if exists
        # -------------------------
        if self.MODEL_PATH.exists():
            self.pipeline = joblib.load(self.MODEL_PATH)
            self.is_trained = True
        else:
            file_path = Path(dataset_path)
            if file_path.exists():
                self.train_from_json(dataset_path)

    def train_from_json(self, dataset_path: str):
        file_path = Path(dataset_path)
        if not file_path.exists():
            raise ValueError(f"Dataset file not found: {dataset_path}")

        data = json.loads(file_path.read_text(encoding="utf-8"))
        texts = [clean_text(d["text"]) for d in data]
        labels = [d["label"] for d in data]

        self.pipeline.fit(texts, labels)
        self.is_trained = True

        # -------------------------
        # Save trained pipeline
        # -------------------------
        self.MODEL_PATH.parent.mkdir(exist_ok=True)
        joblib.dump(self.pipeline, self.MODEL_PATH)

    def predict(self, text: str) -> Dict[str, float]:
        text_clean = clean_text(text)
        if self.is_trained:
            label = self.pipeline.predict([text_clean])[0]
            confidence = float(max(self.pipeline.predict_proba([text_clean])[0]))
        else:
            # fallback if no training data provided
            if "invoice" in text_clean or ("q" in text_clean and "num" in text_clean):
                label = "finance.invoice"
            elif "policy" in text_clean or "hr" in text_clean:
                label = "hr.policy"
            else:
                label = "legal.contract"
            confidence = 0.75

        return {"label": label, "confidence": confidence}
