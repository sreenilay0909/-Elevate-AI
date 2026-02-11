@echo off
echo ========================================
echo    ElevateAI - Starting Project
echo ========================================
echo.

echo Starting Backend Server...
start "ElevateAI Backend" cmd /k "cd backend && start_server.bat"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "ElevateAI Frontend" cmd /k "cd elevateai_-career-enhancement-tool && start_frontend.bat"

echo.
echo ========================================
echo Both servers are starting...
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Check the opened terminal windows for logs
echo ========================================
echo.

pause
