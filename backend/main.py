"""
Main FastAPI application for FAGE Character Generator.
Entry point for the backend API server.
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from config import settings
from api.routes import character, data, actions, system
from utils.logger import setup_logger
from pathlib import Path

# Frontend build location. PyInstaller / launcher can override via env var.
FRONTEND_DIST = Path(
    os.environ.get(
        "FRONTEND_DIST",
        str(Path(__file__).resolve().parent.parent / "frontend" / "dist"),
    )
)

# Setup logger
log_file = Path(settings.LOG_FILE) if settings.LOG_FILE else None
logger = setup_logger("fage", level=settings.LOG_LEVEL, log_file=log_file)


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Add CORS middleware
# NOTE: Current CORS settings allow localhost only for development.
# If deploying remotely or to production, update CORS_ORIGINS in config.py
# to include the production frontend URL (e.g., https://your-domain.com)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# Include routers
app.include_router(
    character.router,
    prefix="/api/characters",
    tags=["characters"]
)

app.include_router(
    data.router,
    prefix="/api/data",
    tags=["data"]
)

app.include_router(
    actions.router,
    prefix="/api",
    tags=["actions"]
)

app.include_router(
    system.router,
    prefix="/api",
    tags=["system"]
)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns API health status.
    """
    return {
        "status": "healthy",
        "version": settings.API_VERSION
    }


# Serve built frontend (production / bundled exe). In dev, run Vite separately.
if FRONTEND_DIST.is_dir():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    _SPA_RESERVED_PREFIXES = ("api/", "docs", "redoc", "openapi.json", "health")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Don't intercept API or auto-generated docs paths.
        if full_path.startswith(_SPA_RESERVED_PREFIXES):
            raise HTTPException(status_code=404)
        # Serve a real file from dist if it exists (favicon, icon, etc).
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        # Otherwise fall back to index.html so Vue Router handles the route.
        return FileResponse(FRONTEND_DIST / "index.html")
else:
    @app.get("/", tags=["root"])
    async def root():
        """Dev fallback when no frontend build is present."""
        return {
            "name": settings.API_TITLE,
            "version": settings.API_VERSION,
            "description": settings.API_DESCRIPTION,
            "docs": "/docs",
            "openapi": "/openapi.json",
            "note": "No frontend/dist found. Run `npm run build` to enable the UI.",
        }


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    logger.warning(f"404 Not Found: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    logger.error(f"500 Internal Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.

    Runs when the server starts.
    """
    logger.info("=" * 60)
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"Docs: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"Log Level: {settings.LOG_LEVEL}")
    logger.info("=" * 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.

    Runs when the server stops.
    """
    logger.info("=" * 60)
    logger.info(f"Shutting down {settings.API_TITLE}")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
