# PyInstaller spec for FAGE Character Generator.
#
# Build:
#   pyinstaller fage.spec --clean
#
# Output:
#   dist/FAGE.exe  (Windows) — single-file bundle
#
# Prerequisites:
#   1. cd frontend && npm run build          (produces frontend/dist)
#   2. cd backend && venv\Scripts\pip install -r requirements.txt pyinstaller
#
# The backend's `python-multipart` package is imported by FastAPI as
# `multipart`; PyInstaller's heuristics sometimes miss it, so it is listed
# in hiddenimports below.

from pathlib import Path

PROJECT_ROOT = Path(SPECPATH)
BACKEND = PROJECT_ROOT / "backend"
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"

if not FRONTEND_DIST.is_dir():
    raise SystemExit(
        "frontend/dist not found. Run `npm run build` in the frontend/ "
        "directory before building the bundle."
    )

datas = [
    # Bundled CSVs + PDF template (read-only; CSVs are also copied to the
    # user data dir on first run by launcher.py).
    (str(BACKEND / "data"), "data"),
    # Built Vue SPA, served by FastAPI as static files.
    (str(FRONTEND_DIST), "frontend/dist"),
]

hiddenimports = [
    "multipart",         # python-multipart, used by FastAPI for form parsing
    "uvicorn.loops.auto",
    "uvicorn.protocols.http.auto",
    "uvicorn.protocols.websockets.auto",
    "uvicorn.lifespan.on",
]

a = Analysis(
    [str(BACKEND / "launcher.py")],
    pathex=[str(BACKEND)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        # Trim some heavyweight optional pandas deps we don't use.
        "matplotlib",
        "tkinter",
        "PyQt5",
        "PyQt6",
        "PySide2",
        "PySide6",
        "IPython",
        "jupyter",
        "notebook",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="FAGE",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,   # keep console for v1 so users see errors; switch to False later
    icon=str(PROJECT_ROOT / "FageIcon2.ico"),
)
