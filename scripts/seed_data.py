"""
Seed and split dataset for training and evaluation.

- Reads: data/samples/training_data.json
- Writes:
    - data/samples/train.json
    - data/samples/eval.json

This script enforces:
- Stratified split by label
- Deterministic output (fixed random seed)
- Basic data validation
"""

import json
import random
from pathlib import Path
from collections import defaultdict

# -------------------------
# Configuration
# -------------------------
RANDOM_SEED = 42
TRAIN_RATIO = 0.7

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "data" / "samples"

SOURCE_FILE = SAMPLES_DIR / "training_data.json"
TRAIN_FILE = SAMPLES_DIR / "train.json"
EVAL_FILE = SAMPLES_DIR / "eval.json"


def main():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f"Source dataset not found: {SOURCE_FILE}")

    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("Dataset must be a non-empty list")

    # -------------------------
    # Basic validation
    # -------------------------
    for i, item in enumerate(data):
        if "text" not in item or "label" not in item:
            raise ValueError(f"Invalid sample at index {i}: {item}")

    # -------------------------
    # Stratified split
    # -------------------------
    random.seed(RANDOM_SEED)

    by_label = defaultdict(list)
    for item in data:
        by_label[item["label"]].append(item)

    train_data = []
    eval_data = []

    for label, items in by_label.items():
        random.shuffle(items)

        split_idx = max(1, int(len(items) * TRAIN_RATIO))

        train_data.extend(items[:split_idx])
        eval_data.extend(items[split_idx:])

    # Final shuffle (important)
    random.shuffle(train_data)
    random.shuffle(eval_data)

    # -------------------------
    # Write outputs
    # -------------------------
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    with open(TRAIN_FILE, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)

    with open(EVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(eval_data, f, indent=2, ensure_ascii=False)

    # -------------------------
    # Summary
    # -------------------------
    print("====================================")
    print("Dataset seeding completed")
    print("====================================")
    print(f"Total samples : {len(data)}")
    print(f"Train samples : {len(train_data)}")
    print(f"Eval samples  : {len(eval_data)}")
    print()

    print("Label distribution (train):")
    _print_distribution(train_data)

    print("\nLabel distribution (eval):")
    _print_distribution(eval_data)


def _print_distribution(dataset):
    dist = defaultdict(int)
    for item in dataset:
        dist[item["label"]] += 1

    for label, count in sorted(dist.items()):
        print(f"  {label:<20} {count}")


if __name__ == "__main__":
    main()
