@echo off
echo ========================================
echo   RESTORE ORIGINAL APP
echo ========================================
echo.
echo This will restore your original app.py
echo.
pause

copy app_original.py app.py

echo.
echo ========================================
echo   RESTORE COMPLETE!
echo ========================================
echo.
echo Your original app.py has been restored.
echo.
echo To run your app:
echo   python app.py
echo.
pause
