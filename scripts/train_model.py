#scripts\train_model.py
from pathlib import Path
import sys

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import joblib
from app.classification.sklearn_model import SklearnClassifier

# -------------------------
# Paths
# -------------------------
DATASET_PATH = Path(__file__).parent.parent / "data" / "samples" / "training_data.json"
MODEL_PATH = Path(__file__).parent.parent / "models" / "trained_pipeline.joblib"

# -------------------------
# Train classifier
# -------------------------
print(f"Loading training data from {DATASET_PATH}")
classifier = SklearnClassifier(dataset_path=str(DATASET_PATH))

# Save trained pipeline
joblib.dump(classifier.pipeline, MODEL_PATH)
print(f"Trained model saved to {MODEL_PATH}")
