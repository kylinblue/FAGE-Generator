"""
Desktop launcher for FAGE Character Generator.

Used as the entry point for the bundled (PyInstaller) build. Configures
the backend to write user data into a per-user OS app-data directory,
binds the server to localhost only, then opens the user's default
browser once the server is ready.

Can also be run directly from a checkout for an end-to-end smoke test
of the bundled flow:

    python backend/launcher.py
"""

import os
import shutil
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8765
APP_NAME = "FAGE"


def app_data_dir() -> Path:
    """Per-user, OS-appropriate writable directory for app data."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
    return base / APP_NAME


def bundle_root() -> Path:
    """Root where read-only bundled resources live (PyInstaller-aware).

    Frozen: PyInstaller's _MEIPASS extraction dir.
    Source: the backend/ directory — matches what we bundle as data.
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent


def frontend_dist() -> Path:
    """Built Vue assets. In frozen mode bundled under _MEIPASS/frontend/dist;
    in source mode at <project_root>/frontend/dist (one level above backend/)."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "frontend" / "dist"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent / "frontend" / "dist"


def seed_user_data(data_dir: Path) -> None:
    """Create user dirs and copy default CSVs on first run."""
    (data_dir / "characters").mkdir(parents=True, exist_ok=True)
    csv_dst = data_dir / "csv"
    if not csv_dst.exists():
        csv_src = bundle_root() / "data" / "csv"
        if csv_src.is_dir():
            shutil.copytree(csv_src, csv_dst)


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) == 0


def open_browser_when_ready(url: str, timeout_s: float = 15.0) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((HOST, PORT), timeout=0.25):
                webbrowser.open(url)
                return
        except OSError:
            time.sleep(0.2)


def main() -> int:
    data_dir = app_data_dir()
    seed_user_data(data_dir)

    # Configure the backend via env vars. pydantic-settings in config.py
    # reads these at import time, so they must be set before importing main.
    os.environ["HOST"] = HOST
    os.environ["PORT"] = str(PORT)
    os.environ["RELOAD"] = "false"
    os.environ["DATA_DIR"] = str(data_dir)
    os.environ["STORAGE_DIR"] = str(data_dir / "characters")
    os.environ["CSV_DIR"] = str(data_dir / "csv")
    os.environ["FRONTEND_DIST"] = str(frontend_dist())
    os.environ["LOG_FILE"] = str(data_dir / "fage.log")
    # Tighten CORS to localhost-only — we're a single-origin app now.
    os.environ["CORS_ORIGINS"] = f'["http://{HOST}:{PORT}"]'

    if port_in_use(PORT):
        print(
            f"ERROR: Port {PORT} is already in use. Close whatever is using "
            f"it (or another running copy of {APP_NAME}) and try again.",
            file=sys.stderr,
        )
        return 1

    # Make `from main import app` work in both source and frozen modes.
    backend_dir = bundle_root() if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Import the app object directly (not as the string "main:app"). This
    # triggers PyInstaller's static analyzer to follow all transitive imports
    # — string-based uvicorn imports would silently leave `main` out of the
    # bundle. Must happen after env vars are set so config.py reads them.
    from main import app  # noqa: E402

    url = f"http://{HOST}:{PORT}"
    threading.Thread(target=open_browser_when_ready, args=(url,), daemon=True).start()
    print(f"Starting {APP_NAME} at {url}")

    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
    return 0


if __name__ == "__main__":
    sys.exit(main())
