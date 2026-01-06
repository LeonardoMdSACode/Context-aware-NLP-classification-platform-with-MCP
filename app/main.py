from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.api.routes import router as api_router

# MCP (embedded mode)
from app.orchestration.mcp_client import start_embedded_mcp_servers, stop_embedded_mcp_servers

from app.logging_config import setup_logging
import logging


def create_app() -> FastAPI:
    """
    Application factory with lifespan handler for startup/shutdown.
    """
    settings = get_settings()
    
    setup_logging()
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Handles startup and shutdown with lifespan."""
        # Startup
        logger.info("Application startup initiated")
        if settings.MCP_EMBEDDED:
            logger.info("Starting embedded MCP servers")
            start_embedded_mcp_servers()
        logger.info("Application startup complete")

        yield  # Control passes to FastAPI for request handling

        # Shutdown
        logger.info("Application shutdown initiated")
        if settings.MCP_EMBEDDED:
            logger.info("Stopping embedded MCP servers")
            stop_embedded_mcp_servers()
        logger.info("Application shutdown complete")

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
        lifespan=lifespan,  # ← attach lifespan handler
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

    return app


# FastAPI entrypoint
app = create_app()
