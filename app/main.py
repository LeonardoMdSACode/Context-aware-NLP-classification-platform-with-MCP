from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.api.routes import router as api_router

# MCP (embedded mode)
from app.orchestration.mcp_client import start_embedded_mcp_servers
from app.orchestration.mcp_client import stop_embedded_mcp_servers


def create_app() -> FastAPI:
    """
    Application factory.

    Ensures:
    - Deterministic startup
    - Clean separation of concerns
    - HF Spaces compatibility
    """

    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
    )

    # -------------------------
    # Middleware
    # -------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # Routes
    # -------------------------
    app.include_router(api_router)

    # -------------------------
    # Lifecycle Events
    # -------------------------
    @app.on_event("startup")
    async def on_startup() -> None:
        """
        Startup logic.

        In HF Spaces:
        - MCP servers are started embedded

        Locally:
        - MCP servers are external (docker-compose)
        """
        if settings.MCP_EMBEDDED:
            start_embedded_mcp_servers()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        """
        Graceful shutdown.
        """
        if settings.MCP_EMBEDDED:
            stop_embedded_mcp_servers()

    return app


# FastAPI entrypoint (required by HF Spaces and uvicorn)
app = create_app()
