@echo off
echo Starting ElevateAI Frontend...
echo.

cd /d "%~dp0"

echo Starting Vite development server...
echo Frontend will be available at http://localhost:3000
echo Press Ctrl+C to stop the server
echo.

npm run dev

pause
