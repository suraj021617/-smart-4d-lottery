@echo off
color 0A
title SMART 4D - Master Fix Tool

:MENU
cls
echo ╔════════════════════════════════════════════════════════╗
echo ║        SMART 4D LOTTERY - MASTER FIX TOOL             ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo  What would you like to do?
echo.
echo  [1] 🔍 Diagnose Issues (Check what's wrong)
echo  [2] 🔧 Fix All Issues (Install dependencies)
echo  [3] 🧹 Cleanup Project (Remove old files)
echo  [4] ▶️  Start Application
echo  [5] 🛑 Kill Running App (If stuck)
echo  [6] 📖 View Troubleshooting Guide
echo  [7] ❌ Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto DIAGNOSE
if "%choice%"=="2" goto FIX
if "%choice%"=="3" goto CLEANUP
if "%choice%"=="4" goto START
if "%choice%"=="5" goto KILL
if "%choice%"=="6" goto GUIDE
if "%choice%"=="7" goto EXIT
goto MENU

:DIAGNOSE
cls
echo Running diagnostics...
echo.
call DIAGNOSE.bat
pause
goto MENU

:FIX
cls
echo Installing dependencies and fixing issues...
echo.
call FIX_ALL_ISSUES.bat
pause
goto MENU

:CLEANUP
cls
echo Cleaning up project...
echo.
call CLEANUP_PROJECT.bat
pause
goto MENU

:START
cls
echo ========================================
echo  Starting Smart 4D Application...
echo ========================================
echo.
echo The app will start on: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
goto MENU

:KILL
cls
echo Killing all Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% equ 0 (
    echo ✅ All Python processes killed
) else (
    echo ℹ️ No Python processes found
)
echo.
pause
goto MENU

:GUIDE
cls
type TROUBLESHOOTING_GUIDE.md
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Thank you for using Smart 4D Master Fix Tool!
echo.
timeout /t 2 >nul
exit

