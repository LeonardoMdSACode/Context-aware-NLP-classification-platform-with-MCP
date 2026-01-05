from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
HISTORY_PATH = BASE_DIR / "data" / "labels.csv"

app = FastAPI(title="History MCP Server")


class RequestModel(BaseModel):
    text: str
    metadata: dict = {}


@app.post("/resolve")
def resolve(request: RequestModel):
    """
    Returns historical label info for a document.
    """

    df = pd.read_csv(HISTORY_PATH)
    # deterministic sample: pick first 5 rows
    history = df.head(5).to_dict(orient="records")

    context = {"historical_labels": history}
    return context
