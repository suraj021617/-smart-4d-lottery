@echo off
title EMERGENCY RESTORE - Smart 4D Lottery
color 0A

echo.
echo  ╔════════════════════════════════════════╗
echo  ║   EMERGENCY RESTORE TO YESTERDAY       ║
echo  ╚════════════════════════════════════════╝
echo.

REM Kill Flask
taskkill /F /IM python.exe >nul 2>&1

REM Restore files
echo  [1] Restoring app.py...
if exist "app_backup.py" (
    copy /Y app_backup.py app.py >nul
    echo      ✓ Done
) else (
    echo      ✗ Backup not found
)

echo  [2] Restoring CSV...
if exist "4d_results_history_backup.csv" (
    copy /Y 4d_results_history_backup.csv 4d_results_history.csv >nul
    echo      ✓ Done
) else if exist "4d_results_history_RESTORED.csv" (
    copy /Y 4d_results_history_RESTORED.csv 4d_results_history.csv >nul
    echo      ✓ Done (from RESTORED)
) else (
    echo      ✗ Backup not found
)

echo  [3] Clearing cache...
rmdir /S /Q __pycache__ >nul 2>&1
rmdir /S /Q utils\__pycache__ >nul 2>&1
echo      ✓ Done

echo.
echo  ╔════════════════════════════════════════╗
echo  ║   ✅ RESTORE COMPLETE!                 ║
echo  ╚════════════════════════════════════════╝
echo.
echo  Now run: python app.py
echo.
pause
