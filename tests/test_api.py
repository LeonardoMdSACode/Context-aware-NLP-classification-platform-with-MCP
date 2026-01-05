import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    json_data = r.json()
    assert "status" in json_data
    assert json_data["status"] == "ok"

def test_classify_basic():
    payload = {"text": "Invoice for Q4 consulting", "metadata": {"source": "email"}}
    r = client.post("/classify", json=payload)
    assert r.status_code == 200
    json_data = r.json()
    assert "label" in json_data
    assert "confidence" in json_data
    assert "abstained" in json_data
    assert "context_used" in json_data

def test_context_endpoint():
    payload = {"text": "Sample document"}
    r = client.post("/context", json=payload)
    assert r.status_code == 200
    json_data = r.json()
    assert "context" in json_data
    assert "sources" in json_data
