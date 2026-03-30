@echo off
title Smart 4D Lottery - RESTORED
color 0A
chcp 65001 >nul

echo.
echo ╔════════════════════════════════════════╗
echo ║   Smart 4D Lottery System              ║
echo ║   RESTORED VERSION                     ║
echo ╚════════════════════════════════════════╝
echo.
echo Starting Flask server...
echo.
echo Open browser: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop
echo.

python app.py

pause
