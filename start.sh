#!/bin/bash
set -e

# HF provides $PORT for the UI
PORT=${PORT:-8501}

echo "Starting FastAPI server in background..."
uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8000 &

echo "Starting Streamlit UI..."
streamlit run ui/streamlit_app.py \
    --server.port $PORT \
    --server.address 0.0.0.0
