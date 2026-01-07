#!/usr/bin/env python
import argparse
import json
from pathlib import Path

import joblib
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"


def load_model():
    model_path = MODELS_DIR / "trained_pipeline.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    return joblib.load(model_path)


def load_dataset(dataset_path: Path):
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    # Hard guard: never evaluate on training data
    if dataset_path.name in {"training_data.json", "train.json"}:
        raise RuntimeError(
            f"Refusing to evaluate on training dataset: {dataset_path.name}"
        )

    with dataset_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    if isinstance(raw, list):
        samples = raw
    elif isinstance(raw, dict) and "samples" in raw:
        samples = raw["samples"]
    else:
        raise ValueError("Unsupported JSON dataset format")

    texts = []
    labels = []

    for i, item in enumerate(samples):
        if "text" not in item or "label" not in item:
            raise ValueError(f"Invalid sample at index {i}: {item}")
        texts.append(item["text"])
        labels.append(item["label"])

    return texts, labels


def evaluate(model, X, y):
    y_pred = model.predict(X)

    acc = accuracy_score(y, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y, y_pred, average="weighted", zero_division=0
    )

    print("====================================")
    print("Offline Evaluation Results")
    print("====================================")
    print(f"Samples  : {len(y)}")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")
    print()
    print("Detailed Classification Report")
    print("------------------------------------")
    print(classification_report(y, y_pred, zero_division=0))


def main():
    parser = argparse.ArgumentParser(
        description="Offline evaluation using held-out JSON dataset"
    )
    parser.add_argument(
        "--data",
        default=str(DATA_DIR / "samples" / "eval.json"),
        help="Path to evaluation dataset (default: data/samples/eval.json)"
    )

    args = parser.parse_args()

    model = load_model()
    X, y = load_dataset(Path(args.data))
    evaluate(model, X, y)


if __name__ == "__main__":
    main()
