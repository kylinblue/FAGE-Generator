"""
System / desktop-integration routes for FAGE Character Generator.

These endpoints assume the backend runs as a *local* process on the same
machine as the user (the packaged desktop app). They open the OS file
manager on the machine running the server — which, for the desktop build,
is the user's own machine. Do not expose these on a remotely hosted
deployment: the folder would open on the server, not the visitor's PC.
"""

import os
import sys
import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException

from config import settings

router = APIRouter()


def _data_dir() -> Path:
    """Resolve the user-facing data directory.

    Prefer the explicit DATA_DIR (set by launcher.py for the bundled app);
    fall back to the parent of STORAGE_DIR (``<data>/characters`` -> ``<data>``)
    so this also works when running from a source checkout.
    """
    if settings.DATA_DIR:
        return Path(settings.DATA_DIR).resolve()
    return Path(settings.STORAGE_DIR).resolve().parent


@router.get("/system/data-dir")
async def get_data_dir():
    """Return the on-disk data directory path (for display / copy-to-clipboard)."""
    return {"path": str(_data_dir())}


@router.post("/system/open-data-dir")
async def open_data_dir():
    """Open the data directory in the OS file manager."""
    path = _data_dir()
    # Be safe on a brand-new install where nothing has been written yet.
    path.mkdir(parents=True, exist_ok=True)

    try:
        if sys.platform == "win32":
            os.startfile(path)  # type: ignore[attr-defined]  # Windows-only; no shell, no injection
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        else:
            subprocess.run(["xdg-open", str(path)], check=True)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not open data directory: {e}",
        )

    return {"opened": str(path)}
