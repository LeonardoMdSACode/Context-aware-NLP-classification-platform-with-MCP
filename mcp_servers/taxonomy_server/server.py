from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import sqlite3
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "taxonomy.sqlite"

app = FastAPI(title="Taxonomy MCP Server")


class RequestModel(BaseModel):
    text: str
    metadata: dict = {}


@app.post("/resolve")
def resolve(request: RequestModel):
    """
    Returns structured taxonomy context for a document.
    """

    # Open SQLite DB (read-only)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Simple deterministic mapping example
    cursor.execute("SELECT category, description FROM taxonomy LIMIT 5;")
    rows = cursor.fetchall()
    conn.close()

    context = {
        "version": "1.0",
        "categories": [{"name": r[0], "description": r[1]} for r in rows],
    }
    return context
