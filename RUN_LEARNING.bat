@echo off
echo ========================================
echo  AUTO LEARNING SYSTEM
echo ========================================
echo.
echo This will check your predictions against
echo actual results from CSV and learn from them
echo.
pause

python auto_learning_system.py

echo.
echo ========================================
echo  Learning Complete!
echo ========================================
echo.
echo Now open your browser and go to:
echo http://127.0.0.1:5000/method-performance
echo.
pause
