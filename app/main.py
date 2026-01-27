# app\main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import logging
from pathlib import Path

from app.config import get_settings
from app.api.routes import router as api_router
from app.orchestration.mcp_client import start_embedded_mcp_servers, stop_embedded_mcp_servers
from app.logging_config import setup_logging


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging()
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Application startup initiated")
        if settings.MCP_EMBEDDED:
            logger.info("Starting embedded MCP servers")
            start_embedded_mcp_servers()
        logger.info("Application startup complete")

        yield

        logger.info("Application shutdown initiated")
        if settings.MCP_EMBEDDED:
            logger.info("Stopping embedded MCP servers")
            stop_embedded_mcp_servers()
        logger.info("Application shutdown complete")

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="0.1.0",
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------
    # Static files and templates
    # -------------------------
    BASE_DIR = Path(__file__).resolve().parent.parent
    app.mount("/static", StaticFiles(directory=BASE_DIR / "ui" / "static"), name="static")
    templates = Jinja2Templates(directory=BASE_DIR / "ui" / "templates")

    @app.get("/", response_class=HTMLResponse)
    async def serve_index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    # API routes
    app.include_router(api_router)

    return app


# Entrypoint
app = create_app()
