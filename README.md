---
title: Context-aware NLP classification platform with MCP
emoji: 🧠
colorFrom: indigo
colorTo: red
sdk: docker
app_file: Dockerfile
pinned: false
license: mit
---

# Context-aware NLP Classification Platform with MCP

## Overview

This repository implements a **context-aware NLP classification platform** that combines a lightweight TF-IDF (Term Frequency–Inverse Document Frequency) + Logistic Regression baseline with optional **LLM-assisted context re-ranking** via MCP (Managed Context Platform). It supports multi-domain classification (finance, HR, legal), structured context resolution, logging, and evaluation.

The platform is modular and can run either **locally in a virtual environment** or inside a **Docker container in Hugging Face Spaces**.

Hugging Face Space: [LeonardoMdSA / Context-aware-NLP-classification-platform-with-MCP](https://huggingface.co/spaces/LeonardoMdSA/Context-aware-NLP-classification-platform-with-MCP)

---

## Repository Structure

```text
Dockerfile
LICENSE
README.md
requirements-dev.txt
requirements.txt

app/
  config.py              # Configuration and settings
  logging_config.py      # Logging configuration
  main.py                # Main entry point for API server
  api/
    routes.py            # FastAPI routes
    schemas.py           # Pydantic schemas
  classification/
    decision.py          # Classification decision & abstention logic
    llm_adapter.py       # Optional LLM integration for context
    model.py             # Abstract classifier orchestration
    preprocess.py        # Text preprocessing and tokenization
    sklearn_model.py     # TF-IDF + Logistic Regression classifier
  context/
    resolver.py          # Context resolution logic
  logging/
    context_log.py       # Context logging to JSON
    inference_log.py     # Inference (label and confidence) logging to JSON

orchestration/
  context_resolver.py    # MCP-based structured context orchestration
  mcp_client.py          # MCP server communication utilities

utils/
  validators.py          # Metadata validation utilities

data/
  samples/
    train.json           # Training samples (small dataset)
    eval.json            # Evaluation samples
    training_data.json   # Full training dataset

docs/
  TECH_DEBT.md           # Technical debt documentation

logs/                     # Runtime logs

mcp_servers/
  history_server/         # Historical label MCP server
    server.py
    data/labels.csv
  policy_server/          # Policy MCP server
    server.py
    data/rules.yaml
  taxonomy_server/        # Taxonomy MCP server
    server.py
    data/taxonomy.sqlite

models/
  trained_pipeline.joblib # Trained sklearn model pipeline

scripts/
  evaluate.py             # Offline evaluation script
  populate_taxonomy.py    # Populate taxonomy.sqlite for MCP
  seed_data.py            # Seed initial data into MCP files
  train_model.py          # Train sklearn model from JSON dataset

tests/
  conftest.py             # Pytest configuration
  test_api.py             # API endpoint tests
  test_classification.py  # Classification module tests
  test_context_resolution.py  # Context resolver tests
  test_mcp_servers.py     # MCP server tests

ui/
  static/
    script.js             # Frontend JS
    style.css             # Frontend CSS
  templates/
    index.html            # Frontend template
```

---

## Installation (Local)

### 1. Clone the repository

```bash
git clone https://github.com/LeonardoMdSACode/Context-aware-NLP-classification-platform-with-MCP.git
cd Context-aware-NLP-classification-platform-with-MCP
```

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for testing and development
```

### 4. Populate MCP Taxonomy (first time setup)

```bash
python scripts/populate_taxonomy.py
```

This populates `mcp_servers/taxonomy_server/data/taxonomy.sqlite`.

### 5. Train the model

```bash
python scripts/train_model.py
```

This trains the TF-IDF + Logistic Regression model and saves it to `models/trained_pipeline.joblib`.

### 6. Evaluate the model

```bash
python scripts/evaluate.py
```

Shows offline evaluation metrics (accuracy, precision, recall, F1-score).

---

## Running the API Locally

### 1. Start the server

```bash
uvicorn app.main:app --reload
```

This runs the FastAPI server at `http://127.0.0.1:8000`.

### 2. Run MCP embedded servers (if using embedded mode)

Embedded MCP servers are started automatically via `app.orchestration.mcp_client.start_embedded_mcp_servers()`.

### 3. Access UI

Open your browser at `http://127.0.0.1:8000` to use the HTML/JS frontend.

### 4. API Endpoints

* `POST /classify` : Send `text` and optional `metadata` to get classification with context.
* Swagger UI: `http://127.0.0.1:8000/docs`

---

## Testing

### 1. Run all tests

```bash
pytest -v
```

### 2. Smoke Test

* Run `test_backend.py` to ensure core API routes respond correctly.
* Check MCP servers respond to `/resolve` endpoints.

### 3. Module-specific tests

* `test_classification.py` → validates `SklearnClassifier` and `LLMAdapter` predictions.
* `test_context_resolution.py` → checks context resolver output.
* `test_mcp_servers.py` → verifies taxonomy, policy, history MCP servers.

---

## How It Works

### 1. Classification Layer

* **Baseline:** `app/classification/sklearn_model.py` → TF-IDF + Logistic Regression
* **LLM-assisted:** `app/classification/llm_adapter.py` → optional MCP context re-ranking
* **Decision logic:** `app/classification/decision.py` → applies confidence, abstention, logging

### 2. Context Resolution

* **Embedded MCP mode:** `app/orchestration/context_resolver.py` loads JSON/SQLite local files
* **Distributed MCP mode:** fetches context from taxonomy, policy, and history MCP servers
* Logs all context resolution for auditability

### 3. Logging

* `app/logging/inference_log.py` → logs every prediction
* `app/logging/context_log.py` → logs context used in classification
* Logs stored as JSON in `logs/`

### 4. MCP Servers

* `taxonomy_server` → serves categories and descriptions from SQLite
* `policy_server` → serves policy rules from YAML
* `history_server` → serves historical label data from CSV
* Communicated via HTTP endpoints

### 5. Scripts

* `train_model.py` → trains and saves the sklearn pipeline
* `evaluate.py` → offline evaluation
* `populate_taxonomy.py` → populates SQLite taxonomy
* `seed_data.py` → seeds MCP JSON files

### 6. Frontend UI

* Simple interface in `ui/templates/index.html`
* Uses JS (`static/script.js`) to call `/classify` endpoint
* Styled via `static/style.css`

---

## Technology Stack

This project implements a **production-style, context-aware NLP classification platform** with classical machine learning, MCP-based context enrichment, and a FastAPI inference layer.

---

### **Core Language & Runtime**

* **Python 3.13**

  * Primary implementation language
  * Virtual environment support (`venv`)
  * Compatible with local execution and Docker

---

### **Machine Learning & NLP**

* **scikit-learn**

  * `TfidfVectorizer` for text feature extraction
  * `LogisticRegression` (multiclass, class-balanced)
  * Optional probability calibration (`CalibratedClassifierCV`)
* **Joblib**

  * Model serialization and loading (`trained_pipeline.joblib`)
* **Classical ML (non-deep learning)**

  * Chosen for interpretability, determinism, and production realism

---

### **Text Representation**

* **TF-IDF (Term Frequency–Inverse Document Frequency)**

  * Unigram and bigram features
  * Sparse vector representation
  * Fast, explainable, and deterministic

---

### **Model Inference & Decision Logic**

* **Custom classification orchestration**

  * Confidence-based routing
  * Abstention handling
  * Deterministic fallback heuristics
* **Context-aware decision layer**

  * Predictions adjusted using MCP-derived signals
* **Inference logging**

  * Inputs, predicted labels, confidence scores, and context

---

### **Context & MCP (Model Context Protocol)**

* **MCP-inspired architecture (local servers)**

  * Context resolved dynamically at inference time
* **Independent MCP servers**

  * **Taxonomy Server** (SQLite-backed document taxonomy)
  * **Policy Server** (YAML-based business rules)
  * **History Server** (CSV-based label history)
* **Context Resolver**

  * Aggregates signals from all MCP servers
  * Injects structured context into the classifier decision flow

---

### **Backend API**

* **FastAPI**

  * REST-based inference service
  * Request/response validation
  * Automatic OpenAPI documentation
* **Uvicorn**

  * ASGI server for local development and deployment
* **Pydantic 2**

  * Strict input/output schemas
  * Validation and type safety

---

### **Frontend (Minimal UI)**

* **HTML / CSS / JavaScript**
* **Jinja2 Templates**
* **FastAPI StaticFiles**
  
  * Lightweight inference interface
  * No Streamlit or Gradio
  * Hugging Face Spaces–compatible

---

### **Persistence & Storage**

* **SQLite**

  * Taxonomy storage (`taxonomy.sqlite`)
* **Filesystem-based storage**

  * Trained models
  * Logs
  * Evaluation artifacts

---

### **Logging & Observability**

* **Structured logging**

  * Inference logs
  * Context resolution logs
* **JSON-based log format**
* Designed to support future:

  * Drift detection
  * Monitoring
  * Alerting

---

### **Evaluation & Experimentation**

* **Offline evaluation scripts**

  * Accuracy, Precision, Recall, F1-score
  * Detailed `classification_report`
* **Separated train / evaluation datasets**
* **Confidence analysis**

  * Used to inspect calibration and overconfidence

---

### **Testing**

* **pytest**

  * API tests
  * Classification logic tests
  * Context resolution tests
  * MCP server tests
* **Smoke tests**

  * End-to-end inference validation
* **Shared fixtures** via `conftest.py`

---

### **DevOps & Packaging**

* **Docker**

  * Reproducible builds
  * Containerized inference service
* **Dependency management**

  * `requirements.txt`
  * `requirements-dev.txt`
* **CI/CD repository structure**

  * GitHub Actions

---

### **Design Philosophy**

* Classical ML over deep learning (intentional)
* Context-aware inference over raw prediction
* Explainability over black-box accuracy
* Production realism over toy demos

---

## Recommendations

* Use a **larger, more diverse dataset** for real-world deployment to avoid overfitting
* Use **sigmoid calibration** for realistic confidence scores
* Keep logs for **auditability** and context traceability
* Run tests regularly with `pytest -v` to ensure stability

---

## References / Docs

* `docs/TECH_DEBT.md` → Technical debt notes and improvement suggestions
* `data/samples/` → Sample training/evaluation datasets
* `models/trained_pipeline.joblib` → Pretrained baseline model

---

## Contact / Author

Repository: [LeonardoMdSACode / Context-aware-NLP-classification-platform-with-MCP](https://github.com/LeonardoMdSACode/Context-aware-NLP-classification-platform-with-MCP)

Hugging Face Space: [LeonardoMdSA / Context-aware-NLP-classification-platform-with-MCP](https://huggingface.co/spaces/LeonardoMdSA/Context-aware-NLP-classification-platform-with-MCP)

---

## MIT License

This project is licensed under the MIT License. See the LICENSE file for details.
