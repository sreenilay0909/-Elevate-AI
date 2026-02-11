@echo off
echo ========================================
echo Installing Phase 2 Dependencies
echo ========================================
echo.

pip install -r requirements-phase2.txt

echo.
echo ========================================
echo Dependencies Installed!
echo ========================================
echo.
echo Next steps:
echo 1. Update backend/.env with SECRET_KEY
echo 2. Run: python setup_database.py
echo 3. Run: python -m uvicorn app.main:app --reload
echo.
pause
