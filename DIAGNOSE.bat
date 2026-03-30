@echo off
echo ========================================
echo  SMART 4D - DIAGNOSTIC REPORT
echo ========================================
echo.

echo [CHECKING PYTHON INSTALLATION]
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found! Install Python 3.8+
    pause
    exit
)
echo.

echo [CHECKING DEPENDENCIES]
echo Checking Flask...
python -c "import flask" 2>nul && echo ✅ Flask installed || echo ❌ Flask missing
echo Checking Pandas...
python -c "import pandas" 2>nul && echo ✅ Pandas installed || echo ❌ Pandas missing
echo Checking Numpy...
python -c "import numpy" 2>nul && echo ✅ Numpy installed || echo ❌ Numpy missing
echo Checking Scikit-learn...
python -c "import sklearn" 2>nul && echo ✅ Scikit-learn installed || echo ❌ Scikit-learn missing
echo.

echo [CHECKING PROJECT FILES]
if exist "app.py" (echo ✅ app.py found) else (echo ❌ app.py missing!)
if exist "4d_results_history.csv" (echo ✅ CSV data found) else (echo ❌ CSV data missing!)
if exist "requirements.txt" (echo ✅ requirements.txt found) else (echo ⚠️ requirements.txt missing)
if exist "utils" (echo ✅ utils folder found) else (echo ❌ utils folder missing!)
if exist "templates" (echo ✅ templates folder found) else (echo ❌ templates folder missing!)
echo.

echo [CHECKING CSV DATA]
if exist "4d_results_history.csv" (
    for %%A in (4d_results_history.csv) do echo CSV Size: %%~zA bytes
    python -c "import pandas as pd; df = pd.read_csv('4d_results_history.csv'); print(f'CSV Rows: {len(df)}'); print(f'CSV Columns: {len(df.columns)}')" 2>nul
) else (
    echo ❌ Cannot check CSV - file missing
)
echo.

echo [CHECKING PORT AVAILABILITY]
netstat -ano | findstr :5000 >nul
if %errorlevel% equ 0 (
    echo ⚠️ Port 5000 is in use
    echo Running processes on port 5000:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do tasklist /FI "PID eq %%a"
) else (
    echo ✅ Port 5000 is available
)
echo.

echo [CHECKING DISK SPACE]
for /f "tokens=3" %%a in ('dir /-c ^| findstr "bytes free"') do echo Free Space: %%a bytes
echo.

echo [PROJECT STATISTICS]
echo Counting files...
for /f %%a in ('dir /b /s *.py ^| find /c /v ""') do echo Python files: %%a
for /f %%a in ('dir /b /s *.html ^| find /c /v ""') do echo HTML files: %%a
for /f %%a in ('dir /b /s *.csv ^| find /c /v ""') do echo CSV files: %%a
echo.

echo [CHECKING FOR ISSUES]
if exist ".history" (
    for /f %%a in ('dir /b /a .history ^| find /c /v ""') do (
        if %%a gtr 50 (
            echo ⚠️ Too many history files: %%a files
            echo Recommendation: Run CLEANUP_PROJECT.bat
        )
    )
)

if exist "__pycache__" (
    echo ⚠️ Python cache exists - may cause issues
    echo Recommendation: Delete __pycache__ folder
)
echo.

echo ========================================
echo  DIAGNOSTIC COMPLETE
echo ========================================
echo.
echo RECOMMENDATIONS:
echo 1. If any ❌ errors above, run FIX_ALL_ISSUES.bat
echo 2. If port 5000 in use, kill the process or use different port
echo 3. If too many files, run CLEANUP_PROJECT.bat
echo.
pause
