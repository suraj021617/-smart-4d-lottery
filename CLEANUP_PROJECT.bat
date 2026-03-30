@echo off
echo ========================================
echo  PROJECT CLEANUP SCRIPT
echo ========================================
echo.
echo This will remove:
echo - Old backup files
echo - History files
echo - Cache files
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/4] Removing old app backups...
del /q app_20*.py 2>nul
echo ✅ Done

echo.
echo [2/4] Cleaning history folder...
if exist ".history" (
    echo Found .history folder with %dir /b /a .history 2^>nul ^| find /c /v ""% files
    rmdir /s /q .history
    echo ✅ Removed
) else (
    echo ℹ️ No .history folder found
)

echo.
echo [3/4] Removing Python cache...
if exist "__pycache__" rmdir /s /q __pycache__
if exist "utils\__pycache__" rmdir /s /q utils\__pycache__
echo ✅ Cache cleared

echo.
echo [4/4] Removing duplicate CSV files...
del /q 4d_results_history_backup*.csv 2>nul
del /q 4d_results_history_RESTORED*.csv 2>nul
echo ✅ Done

echo.
echo ========================================
echo  ✅ CLEANUP COMPLETE!
echo ========================================
echo.
echo Your project is now cleaner and faster!
echo.
pause
