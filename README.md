---
title: Context-aware NLP classification platform with MCP
emoji: 🧠
colorFrom: red
colorTo: deep red
sdk: docker
app_file: Dockerfile
pinned: false
license: mit
---

# Under construction...

venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
streamlit run ui/streamlit_app.py --server.port 8501 --server.address 127.0.0.1

### Tests
pytest -v
Or manual smoke test in test_backend.py

## Initial struture

Context-aware NLP classification platform with MCP/
│
├── Dockerfile                  # Root-level (HF Spaces compatible)
├── docker-compose.yml           # Local multi-service orchestration
│
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── orchestration/
│   │   ├── mcp_client.py
│   │   ├── context_resolver.py
│   │   └── fallback.py
│   │
│   ├── classification/
│   │   ├── preprocess.py
│   │   ├── model.py
│   │   ├── sklearn_model.py
│   │   ├── llm_adapter.py
│   │   └── decision.py
│   │
│   ├── logging/
│   │   ├── context_log.py
│   │   └── inference_log.py
│   │
│   └── utils/
│       └── validators.py
│
├── mcp_servers/
│   ├── taxonomy_server/
│   │   ├── server.py
│   │   └── data/
│   │       └── taxonomy.sqlite
│   │
│   ├── policy_server/
│   │   ├── server.py
│   │   └── data/
│   │       └── rules.yaml
│   │
│   └── history_server/
│       ├── server.py
│       └── data/
│           └── labels.csv
│
├── ui/
│   └── streamlit_app.py
│
├── tests/
│   ├── test_mcp_servers.py
│   ├── test_context_resolution.py
│   ├── test_classification.py
│   └── test_fallbacks.py
│
├── scripts/
│   ├── train_model.py
│   ├── evaluate.py
│   └── seed_data.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
