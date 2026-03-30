@echo off
cls
echo ================================================================================
echo          SMART 4D LOTTERY PREDICTION SYSTEM - STARTING SERVER
echo ================================================================================
echo.

echo [1] Checking Python environment...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python found
echo.

echo [2] Testing imports...
python -c "import flask, pandas, numpy" 2>nul
if errorlevel 1 (
    echo [ERROR] Required packages not installed!
    echo Installing packages...
    pip install flask pandas numpy scikit-learn
)
echo [OK] All packages available
echo.

echo [3] Testing decision-helper route...
python test_decision_helper.py | findstr "SUCCESS ERROR"
echo.

echo ================================================================================
echo                         STARTING FLASK SERVER
echo ================================================================================
echo.
echo Server will start on: http://127.0.0.1:5000
echo.
echo Available routes:
echo   - http://127.0.0.1:5000/
echo   - http://127.0.0.1:5000/decision-helper
echo   - http://127.0.0.1:5000/pattern-analyzer
echo   - http://127.0.0.1:5000/ultimate-predictor
echo   - http://127.0.0.1:5000/past-results
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================
echo.

python app.py
