#!/usr/bin/env bash
# ============================================================================
# FAGE Character Generator - Development Server Launcher (macOS / Linux)
# Starts both Backend and Frontend using concurrently
# Press Ctrl+C to stop both servers
# ============================================================================

set -e

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

print_header "FAGE Character Generator
 Starting Development Servers..."

if ! command -v npm >/dev/null 2>&1; then
    err "npm not found!"
    echo "Please install Node.js 20+ from https://nodejs.org/"
    exit 1
fi

# Root dependencies (concurrently lives here)
if [ ! -d "node_modules" ]; then
    echo "[WARN] Root dependencies not found!"
    echo "Running: npm install"
    echo
    npm install
    echo
fi

# Backend venv must exist (Unix layout)
if [ ! -x "backend/venv/bin/python" ]; then
    err "Backend virtual environment not found!"
    echo "Run: ./setup.sh"
    exit 1
fi

# Frontend deps must exist
if [ ! -d "frontend/node_modules" ]; then
    err "Frontend dependencies not found!"
    echo "Run: ./setup.sh"
    exit 1
fi

echo "Starting servers with concurrently..."
print_header "Servers will start on:"
cat <<'EOF'
 Frontend: http://localhost:5173
 Backend:  http://localhost:8000
 API Docs: http://localhost:8000/docs
EOF
echo
echo "Press Ctrl+C to stop all servers"
echo

# Use npx concurrently directly so we don't depend on the Windows-specific
# venv path baked into package.json's "dev:backend" script.
npx --no-install concurrently \
    -n backend,frontend \
    -c cyan,green \
    --kill-others-on-fail \
    "cd backend && ./venv/bin/python main.py" \
    "cd frontend && npm run dev"

print_header "Servers stopped"
