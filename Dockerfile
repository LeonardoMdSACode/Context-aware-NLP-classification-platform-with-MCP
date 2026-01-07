FROM python:3.11-slim

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# -------------------------
# Python dependencies
# -------------------------
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn[standard] \
    pydantic-settings \
    pydantic \
    requests \
    scikit-learn==1.8.0 \
    python-multipart \
    joblib \
    jinja2

# -------------------------
# Copy application
# -------------------------
COPY . /app

# -------------------------
# Environment (HF Spaces)
# -------------------------
ENV ENV=hf_spaces
ENV DEBUG=False
ENV MCP_EMBEDDED=True
ENV ENABLE_ABSTENTION=False
ENV API_HOST=0.0.0.0
ENV API_PORT=7860

# HF default port
EXPOSE 7860

# -------------------------
# Run FastAPI directly
# -------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
