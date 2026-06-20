@echo off
REM ============================================================================
REM FAGE Character Generator - Initial Setup Script
REM Sets up backend virtual environment and frontend dependencies
REM ============================================================================

echo.
echo ========================================
echo  FAGE Character Generator - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.11 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js 20+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/5] Setting up Backend...
echo.

REM Create backend virtual environment
if exist "backend\venv" (
    echo   - Virtual environment already exists, skipping creation
) else (
    echo   - Creating virtual environment...
    cd backend
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo   - Virtual environment created
)

echo.
echo [2/5] Installing Backend Dependencies...
echo.
cd backend
call venv\Scripts\activate.bat
echo   - Installing Python packages...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo   - Backend dependencies installed

echo.
echo [3/5] Installing Root Dependencies (concurrently)...
echo.
echo   - Running npm install at root...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install root dependencies!
    pause
    exit /b 1
)
echo   - Root dependencies installed (concurrently)

echo.
echo [4/5] Installing Frontend Dependencies...
echo.
cd frontend
echo   - Running npm install...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies!
    cd ..
    pause
    exit /b 1
)
cd ..
echo   - Frontend dependencies installed

echo.
echo [5/5] Creating environment files...
echo.

REM Create backend .env if it doesn't exist
if not exist "backend\.env" (
    echo   - Creating backend/.env from example...
    copy backend\.env.example backend\.env >nul 2>&1
    if exist "backend\.env" (
        echo   - Created backend/.env
    ) else (
        echo   - No .env.example found, skipping
    )
) else (
    echo   - backend/.env already exists, skipping
)

REM Check frontend .env files
if not exist "frontend\.env.development" (
    echo   - frontend/.env.development already exists
) else (
    echo   - frontend/.env.development found
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo  Next steps:
echo.
echo  1. Start development servers (RECOMMENDED):
echo     start-dev.bat
echo     OR: npm run dev
echo.
echo  2. Or start manually:
echo     Terminal 1: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
echo     Terminal 2: cd frontend ^&^& npm run dev
echo.
echo  3. Access the app:
echo     Frontend: http://localhost:5173
echo     Backend:  http://localhost:8000
echo     API Docs: http://localhost:8000/docs
echo.
echo  Note: Press Ctrl+C once to stop all servers cleanly
echo.
echo ========================================
echo.
pause
