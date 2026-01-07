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

# Under construction...

venv\Scripts\activate

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### Tests

pytest -v

Or manual smoke test in test_backend.py


### Train model

python scripts/train_model.py

## Initial struture

Context-aware NLP classification platform with MCP/
├─ Dockerfile
├─ docker-compose.yml
├─ LICENSE
├─ README.md
├─ requirements-dev.txt
├─ requirements.txt
├─ start.sh
├─ test_backend.py
├─ app/
│  ├─ config.py
│  ├─ logging_config.py
│  ├─ main.py                  # FastAPI entrypoint
│  ├─ api/
│  │  ├─ routes.py             # API endpoints (e.g., /predict)
│  │  └─ schemas.py
│  ├─ classification/
│  │  ├─ decision.py
│  │  ├─ llm_adapter.py
│  │  ├─ model.py
│  │  ├─ preprocess.py
│  │  └─ sklearn_model.py
│  ├─ context/
│  │  └─ resolver.py
│  ├─ logging/
│     ├─ context_log.py
│     └─ inference_log.py
├─ orchestration/
│  ├─ context_resolver.py
│  └─ mcp_client.py
├─ utils/
│  └─ validators.py
├─ data/
│  ├─ mcp/
│  │  ├─ history.json
│  │  ├─ policies.json
│  │  └─ taxonomy.json
│  ├─ processed/
│  ├─ raw/
│  └─ samples/
│     └─ training_data.json
├─ docs/
│  └─ TECH_DEBT.md
├─ logs/
├─ mcp_servers/
│  ├─ history_server/
│  │  ├─ server.py
│  │  └─ data/
│  │     └─ labels.csv
│  ├─ policy_server/
│  │  ├─ server.py
│  │  └─ data/
│  │     └─ rules.yaml
│  └─ taxonomy_server/
│     ├─ server.py
│     └─ data/
├─ models/
│  └─ trained_pipeline.joblib
├─ scripts/
│  ├─ evaluate.py
│  ├─ seed_data.py
│  └─ train_model.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_api.py
│  ├─ test_classification.py
│  ├─ test_context_resolution.py
│  └─ test_mcp_servers.py
└─ ui/
   ├─ static/
   │   ├─ style.css
   │   └─ script.js
   └─ templates/
       └─ index.html
