@echo off
REM ============================================================================
REM FAGE Character Generator - Development Server Launcher
REM Starts both Backend and Frontend using npm + concurrently
REM Press Ctrl+C to stop both servers
REM ============================================================================

echo.
echo ========================================
echo  FAGE Character Generator
echo  Starting Development Servers...
echo ========================================
echo.

REM Check Node.js and npm
where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    echo Please install Node.js 20+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if root dependencies installed (concurrently)
if not exist "node_modules" (
    echo [WARN] Root dependencies not found!
    echo Running: npm install
    echo.
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
    echo.
)

REM Check backend venv
if not exist "backend\venv\Scripts\python.exe" (
    echo [ERROR] Backend virtual environment not found!
    echo Run: setup.bat
    pause
    exit /b 1
)

REM Check frontend dependencies
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not found!
    echo Run: setup.bat
    pause
    exit /b 1
)

echo Starting servers with npm...
echo.
echo ========================================
echo  Servers will start on:
echo ========================================
echo  Frontend: http://localhost:5173
echo  Backend:  http://localhost:8000
echo  API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop all servers
echo.

REM Run npm dev script (uses concurrently)
call npm run dev

REM This line will execute after Ctrl+C
echo.
echo ========================================
echo  Servers stopped
echo ========================================
echo.
pause
