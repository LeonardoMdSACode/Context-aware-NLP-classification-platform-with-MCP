from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent
RULES_PATH = BASE_DIR / "data" / "rules.yaml"

app = FastAPI(title="Policy MCP Server")


class RequestModel(BaseModel):
    text: str
    metadata: dict = {}


@app.post("/resolve")
def resolve(request: RequestModel):
    """
    Returns policy rules relevant to a document.
    """

    with open(RULES_PATH, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    # Simple deterministic selection
    context = {"policies": rules.get("policies", {})}
    return context
