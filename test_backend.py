# Manual smoke test of backend

import requests
import json

API_URL = "http://127.0.0.1:8000"

# Sample document
document_text = "Invoice for Q4 2025: total amount $4,500."

# Optional metadata
metadata = {
    "department": "finance",
    "priority": "high"
}

payload = {
    "text": document_text,
    "metadata": metadata
}


def test_classify():
    try:
        response = requests.post(f"{API_URL}/classify", json=payload, timeout=30)
        response.raise_for_status()
        print("Classification Result:")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print("Classification test failed:", str(e))


def test_context():
    try:
        # POST to /context with JSON body
        response = requests.post(f"{API_URL}/context", json=payload, timeout=30)
        response.raise_for_status()
        print("\nContext Result:")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print("Context test failed:", str(e))


def test_predict():
    try:
        # GET to /predict with query param
        response = requests.get(f"{API_URL}/predict", params={"query": document_text}, timeout=30)
        response.raise_for_status()
        print("\nPredict Result (GET /predict):")
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print("Predict test failed:", str(e))


if __name__ == "__main__":
    print("Testing /classify endpoint...")
    test_classify()
    print("\nTesting /context endpoint...")
    test_context()
    print("\nTesting /predict endpoint...")
    test_predict()
