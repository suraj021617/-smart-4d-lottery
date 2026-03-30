@echo off
echo ========================================
echo  RESTORING PROJECT TO YESTERDAY STATE
echo ========================================
echo.

REM Stop Flask if running
echo [1/5] Stopping Flask server...
taskkill /F /IM python.exe 2>nul
timeout /t 2 >nul

REM Backup current state first
echo [2/5] Backing up current state...
copy app.py app_before_restore.py >nul 2>&1
copy 4d_results_history.csv 4d_results_history_before_restore.csv >nul 2>&1

REM Restore from git (safe method - doesn't lose uncommitted work)
echo [3/5] Restoring from git backup...
git stash
git reset --hard d96505c

REM Restore CSV if backup exists
echo [4/5] Restoring CSV data...
if exist "4d_results_history_backup.csv" (
    copy /Y 4d_results_history_backup.csv 4d_results_history.csv >nul
    echo    ✓ CSV restored from backup
) else (
    echo    ⚠ No CSV backup found, using git version
)

REM Clear Python cache
echo [5/5] Clearing cache...
if exist "__pycache__" rmdir /S /Q __pycache__ >nul 2>&1
if exist "utils\__pycache__" rmdir /S /Q utils\__pycache__ >nul 2>&1

echo.
echo ========================================
echo  ✅ RESTORE COMPLETE!
echo ========================================
echo.
echo Your project has been restored to yesterday's working state.
echo.
echo To start the app:
echo    python app.py
echo.
echo If you want to undo this restore:
echo    git reset --hard ab70bb9
echo.
pause
