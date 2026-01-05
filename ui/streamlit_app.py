import streamlit as st
import requests
from pathlib import Path
from app.config import get_settings

settings = get_settings()

# -------------------------
# Helpers
# -------------------------
API_URL = "http://127.0.0.1:8000"  # Adjust for HF Spaces if needed

def classify_document(text: str, metadata: dict = None) -> dict:
    payload = {"text": text, "metadata": metadata or {}}
    response = requests.post(f"{API_URL}/classify", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

def inspect_context(text: str, metadata: dict = None) -> dict:
    payload = {"text": text, "metadata": metadata or {}}
    response = requests.post(f"{API_URL}/context", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="Context-Aware NLP Classifier", layout="wide")
st.title("Context-Aware Document Classification")

st.markdown(
    """
This app demonstrates **classification with MCP context**.
- Upload a document or paste text
- See the predicted label, confidence, and used context
"""
)

text_input = st.text_area("Document Text", height=200)

metadata_input = st.text_area(
    "Optional Metadata (JSON)", "{}"
)

if st.button("Classify"):
    if not text_input.strip():
        st.warning("Please provide document text.")
    else:
        try:
            import json
            metadata = json.loads(metadata_input) if metadata_input.strip() else {}
        except Exception:
            st.error("Invalid metadata JSON.")
            metadata = {}

        with st.spinner("Fetching context and classifying..."):
            classification_result = classify_document(text_input, metadata)
            context_result = inspect_context(text_input, metadata)

        st.subheader("Classification Result")
        st.write(f"**Label:** {classification_result.get('label')}")
        st.write(f"**Confidence:** {classification_result.get('confidence')}")
        st.write(f"**Abstained:** {classification_result.get('abstained')}")

        st.subheader("Context Used")
        st.json(context_result.get("context"))

        st.subheader("Sources Consulted")
        st.write(context_result.get("sources"))
