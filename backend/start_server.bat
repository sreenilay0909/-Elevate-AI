@echo off
echo Starting ElevateAI Backend Server...
echo.

cd /d "%~dp0"

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Warning: Virtual environment not found
)

echo.
echo Starting FastAPI server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
