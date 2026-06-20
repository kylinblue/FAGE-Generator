@echo off
echo ================================================
echo FAGE Character Generator - Starting Backend API
echo ================================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

venv\Scripts\python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
