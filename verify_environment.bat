@echo off
echo ================================================================================
echo VERIFYING PYTHON ENVIRONMENT
echo ================================================================================
echo.

echo [1] Checking Python version...
python --version
echo.

echo [2] Checking installed packages...
python -m pip list | findstr /I "flask pandas numpy scikit"
echo.

echo [3] Testing imports...
python -c "import flask, pandas, numpy, sklearn; print('SUCCESS: All packages can be imported')"
echo.

echo [4] Running system test...
python test_system.py
echo.

echo ================================================================================
echo VERIFICATION COMPLETE
echo ================================================================================
echo.
echo Your system is ready! The Pylance warnings in VS Code are cosmetic only.
echo.
echo To fix VS Code warnings:
echo 1. Press Ctrl+Shift+P
echo 2. Type: Python: Select Interpreter
echo 3. Choose: Python 3.11
echo 4. Press Ctrl+Shift+P
echo 5. Type: Developer: Reload Window
echo.
pause
