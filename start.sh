#!/bin/bash
set -e

# -------------------------
# Start FastAPI backend
# -------------------------
echo "Starting FastAPI server..."
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload &

# -------------------------
# Start Streamlit frontend
# -------------------------
echo "Starting Streamlit UI..."
streamlit run ui/streamlit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 &

# -------------------------
# Keep container alive
# -------------------------
wait
