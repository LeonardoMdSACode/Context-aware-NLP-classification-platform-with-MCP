# Base Image
# -------------------------
FROM python:3.11-slim

# System Dependencies
# -------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Working Directory
# -------------------------
WORKDIR /app

# Copy Repo Files
# -------------------------
COPY . /app

# Python Dependencies
# -------------------------
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    streamlit \
    pydantic-settings \
    pydantic \
    requests \
    scikit-learn \
    transformers \
    python-multipart

# Environment Variables
# -------------------------
ENV ENV=hf_spaces
ENV DEBUG=False
ENV MCP_EMBEDDED=True
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Expose Ports
# -------------------------
# FastAPI API
EXPOSE 8000
# Streamlit UI
EXPOSE 8501

# Entrypoint
# -------------------------
# Use a small shell script to launch both backend and frontend
# in the same container (HF Spaces does not support docker-compose)
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
