@echo off
echo ========================================
echo  MANUAL RESTORE (Using Backup Files)
echo ========================================
echo.

REM Stop Flask
echo [1/4] Stopping Flask server...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Backup current state
echo [2/4] Backing up current broken state...
copy app.py app_broken_backup.py >nul 2>&1
copy 4d_results_history.csv 4d_results_history_broken.csv >nul 2>&1

REM Restore from backup files
echo [3/4] Restoring from backup files...

if exist "app_backup.py" (
    copy /Y app_backup.py app.py >nul
    echo    ✓ app.py restored
) else if exist "app.py.backup" (
    copy /Y app.py.backup app.py >nul
    echo    ✓ app.py restored from .backup
) else (
    echo    ✗ No app.py backup found!
)

if exist "4d_results_history_backup.csv" (
    copy /Y 4d_results_history_backup.csv 4d_results_history.csv >nul
    echo    ✓ CSV restored
) else if exist "4d_results_history_RESTORED.csv" (
    copy /Y 4d_results_history_RESTORED.csv 4d_results_history.csv >nul
    echo    ✓ CSV restored from RESTORED version
) else (
    echo    ✗ No CSV backup found!
)

REM Clear cache
echo [4/4] Clearing Python cache...
if exist "__pycache__" rmdir /S /Q __pycache__ >nul 2>&1
if exist "utils\__pycache__" rmdir /S /Q utils\__pycache__ >nul 2>&1

echo.
echo ========================================
echo  ✅ MANUAL RESTORE COMPLETE!
echo ========================================
echo.
echo Files restored from backup.
echo.
echo To start the app:
echo    python app.py
echo.
pause
