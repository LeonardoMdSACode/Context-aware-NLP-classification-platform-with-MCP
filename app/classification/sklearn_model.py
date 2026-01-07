from pathlib import Path
import joblib
import json
import re
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from typing import Dict
import os

# -------------------------
# Preprocessing
# -------------------------
try:
    from app.classification.preprocess import clean_text as external_clean_text
    clean_text = external_clean_text
except ImportError:
    def clean_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r"\d+", "NUM", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[\x00-\x1f]+", "", text)
        return text.strip()


class SklearnClassifier:
    """
    Lightweight TF-IDF + Logistic Regression classifier for finance/hr/legal.
    """

    # Make MODEL_PATH absolute relative to project root
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    MODEL_PATH = PROJECT_ROOT / "models" / "trained_pipeline.joblib"

    def __init__(self, dataset_path: str = None):
        if dataset_path is None:
            dataset_path = self.PROJECT_ROOT / "data" / "samples" / "training_data.json"
        else:
            dataset_path = Path(dataset_path)

        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=500, class_weight='balanced', C=1.0))
        ])
        self.is_trained = False

        # -------------------------
        # Load trained model if exists
        # -------------------------
        if self.MODEL_PATH.exists():
            self.pipeline = joblib.load(self.MODEL_PATH)
            self.is_trained = True
        elif dataset_path.exists():
            self.train_from_json(dataset_path)
        else:
            print(f"[Warning] No trained model or dataset found. Using fallback logic.")

    def train_from_json(self, dataset_path: Path):
        data = json.loads(dataset_path.read_text(encoding="utf-8"))
        texts = [clean_text(d["text"]) for d in data]
        labels = [d["label"] for d in data]

        self.pipeline.fit(texts, labels)
        self.is_trained = True

        # Save model
        self.MODEL_PATH.parent.mkdir(exist_ok=True, parents=True)
        joblib.dump(self.pipeline, self.MODEL_PATH)

    def predict(self, text: str) -> Dict[str, float]:
        text_clean = clean_text(text)
        if self.is_trained:
            try:
                label = self.pipeline.predict([text_clean])[0]
                # fallback if pipeline has no predict_proba (safety)
                try:
                    confidence = float(max(self.pipeline.predict_proba([text_clean])[0]))
                except Exception:
                    confidence = 0.8
            except Exception as e:
                print("[Error] Sklearn prediction failed:", e)
                label = "unknown"
                confidence = 0.3
        else:
            # fallback heuristic
            if "invoice" in text_clean or ("q" in text_clean and "num" in text_clean):
                label = "finance.invoice"
            elif "policy" in text_clean or "hr" in text_clean:
                label = "hr.policy"
            else:
                label = "legal.contract"
            confidence = 0.3

        return {"label": label, "confidence": confidence}


# -------------------------
# Quick sanity check when run directly
# -------------------------
if __name__ == "__main__":
    clf = SklearnClassifier()
    print("Is trained?", clf.is_trained)
    samples = [
        "Invoice for Q3 2025 amount 23923 $",
        "HR policy update for employees",
        "Signed legal contract for vendor"
    ]
    for s in samples:
        print(s, "->", clf.predict(s))
