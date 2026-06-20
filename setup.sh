#!/usr/bin/env bash
# ============================================================================
# FAGE Character Generator - Initial Setup Script (macOS / Linux)
# Sets up backend virtual environment and frontend dependencies
# ============================================================================

set -e

# Resolve project root (directory containing this script) so the script works
# regardless of where it is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_header() {
    echo
    echo "========================================"
    echo " $1"
    echo "========================================"
    echo
}

err() {
    echo "[ERROR] $1" >&2
}

print_header "FAGE Character Generator - Setup"

# Pick a Python interpreter (prefer python3)
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    err "Python not found!"
    echo "Please install Python 3.11 or higher from https://www.python.org/"
    exit 1
fi

if ! command -v node >/dev/null 2>&1; then
    err "Node.js not found!"
    echo "Please install Node.js 20+ from https://nodejs.org/"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    err "npm not found!"
    echo "Please install Node.js 20+ from https://nodejs.org/"
    exit 1
fi

echo "[1/5] Setting up Backend..."
echo

if [ -d "backend/venv" ]; then
    echo "  - Virtual environment already exists, skipping creation"
else
    echo "  - Creating virtual environment..."
    (cd backend && "$PYTHON_BIN" -m venv venv)
    echo "  - Virtual environment created"
fi

echo
echo "[2/5] Installing Backend Dependencies..."
echo

# Activate venv for this subshell scope
# shellcheck disable=SC1091
source backend/venv/bin/activate
echo "  - Installing Python packages..."
python -m pip install --upgrade pip --quiet
pip install -r backend/requirements.txt
deactivate
echo "  - Backend dependencies installed"

echo
echo "[3/5] Installing Root Dependencies (concurrently)..."
echo
echo "  - Running npm install at root..."
npm install
echo "  - Root dependencies installed (concurrently)"

echo
echo "[4/5] Installing Frontend Dependencies..."
echo
(cd frontend && echo "  - Running npm install..." && npm install)
echo "  - Frontend dependencies installed"

echo
echo "[5/5] Creating environment files..."
echo

if [ ! -f "backend/.env" ]; then
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "  - Created backend/.env from example"
    else
        echo "  - No .env.example found, skipping"
    fi
else
    echo "  - backend/.env already exists, skipping"
fi

if [ -f "frontend/.env.development" ]; then
    echo "  - frontend/.env.development found"
else
    echo "  - frontend/.env.development not present (frontend may use defaults)"
fi

print_header "Setup Complete!"
cat <<'EOF'
 Next steps:

 1. Start development servers (RECOMMENDED):
    ./start-dev.sh

 2. Or start manually:
    Terminal 1: cd backend && source venv/bin/activate && python main.py
    Terminal 2: cd frontend && npm run dev

 3. Access the app:
    Frontend: http://localhost:5173
    Backend:  http://localhost:8000
    API Docs: http://localhost:8000/docs

 Note: Press Ctrl+C once to stop all servers cleanly
EOF
echo
