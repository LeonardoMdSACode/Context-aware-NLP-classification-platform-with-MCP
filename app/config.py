from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings  # updated for Pydantic v2
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized application configuration.

    Designed to work in:
    - Local development
    - Docker / docker-compose
    - Hugging Face Spaces
    """

    # -------------------------
    # Environment
    # -------------------------
    ENV: str = Field(default="local", description="Execution environment")
    DEBUG: bool = Field(default=False)

    # -------------------------
    # API
    # -------------------------
    APP_NAME: str = "Context-Aware NLP Classification Platform"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # -------------------------
    # Paths
    # -------------------------
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    DATA_DIR: Path = BASE_DIR / "data"
    MODEL_DIR: Path = BASE_DIR / "models"
    LOG_DIR: Path = BASE_DIR / "logs"

    # -------------------------
    # Classification
    # -------------------------
    DEFAULT_MODEL: str = "sklearn"
    CONFIDENCE_THRESHOLD: float = 0.6
    ENABLE_ABSTENTION: bool = True

    # -------------------------
    # MCP (Model Context Protocol)
    # -------------------------
    MCP_TIMEOUT_SECONDS: float = 5.0
    MCP_FAIL_FAST: bool = False

    # Embedded MCP (HF Spaces)
    MCP_EMBEDDED: bool = True

    # Local MCP JSON files for embedded context (used if MCP_EMBEDDED=True)
    MCP_TAXONOMY_URL: str = str(DATA_DIR / "mcp/taxonomy.json")
    MCP_POLICY_URL: str = str(DATA_DIR / "mcp/policies.json")
    MCP_HISTORY_URL: str = str(DATA_DIR / "mcp/history.json")

    # Local / distributed MCP (docker-compose) fallback URLs
    MCP_DISTRIBUTED_TAXONOMY_URL: str = "http://taxonomy-server:7001"
    MCP_DISTRIBUTED_POLICY_URL: str = "http://policy-server:7002"
    MCP_DISTRIBUTED_HISTORY_URL: str = "http://history-server:7003"

    # -------------------------
    # Logging
    # -------------------------
    LOG_LEVEL: str = "INFO"
    LOG_CONTEXT_USAGE: bool = True
    LOG_INFERENCE: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings accessor.
    Ensures consistent config across the app.
    """
    settings = Settings()

    # Ensure required directories exist (safe for HF Spaces)
    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
    settings.MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Ensure MCP data folder exists
    (settings.DATA_DIR / "mcp").mkdir(parents=True, exist_ok=True)

    return settings
