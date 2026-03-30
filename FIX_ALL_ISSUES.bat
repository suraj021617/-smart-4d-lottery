@echo off
echo ========================================
echo  SMART 4D - COMPLETE FIX SCRIPT
echo ========================================
echo.

echo [1/5] Installing Python dependencies...
pip install Flask==2.3.3 pandas==2.0.3 numpy==1.24.3 scikit-learn==1.3.0 --upgrade
echo.

echo [2/5] Checking CSV data file...
if exist "4d_results_history.csv" (
    echo ✅ CSV file found
) else (
    echo ❌ CSV file missing! Please add 4d_results_history.csv
    pause
    exit
)
echo.

echo [3/5] Creating backup of current app.py...
copy app.py app_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.py
echo ✅ Backup created
echo.

echo [4/5] Clearing Python cache...
if exist "__pycache__" rmdir /s /q __pycache__
if exist "utils\__pycache__" rmdir /s /q utils\__pycache__
echo ✅ Cache cleared
echo.

echo [5/5] Testing Flask installation...
python -c "import flask; print('✅ Flask version:', flask.__version__)"
python -c "import pandas; print('✅ Pandas version:', pandas.__version__)"
python -c "import numpy; print('✅ Numpy version:', numpy.__version__)"
python -c "import sklearn; print('✅ Scikit-learn version:', sklearn.__version__)"
echo.

echo ========================================
echo  ✅ ALL FIXES COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python app.py
echo 2. Open: http://127.0.0.1:5000
echo.
pause
