# Base Image
FROM python:3.11-slim

# System Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Working Directory
WORKDIR /app

# Copy Repo Files
COPY . /app

# Python Dependencies
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
ENV ENV=hf_spaces
ENV DEBUG=False
ENV MCP_EMBEDDED=True
ENV API_HOST=127.0.0.1
ENV API_PORT=8000

# Expose only HF port (Streamlit)
EXPOSE 8501

# Entrypoint
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
ENTRYPOINT ["/app/start.sh"]
