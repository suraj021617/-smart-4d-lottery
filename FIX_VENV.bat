@echo off
echo Fixing Virtual Environment...

REM Remove old broken venv
if exist .venv rmdir /s /q .venv

REM Create new venv with correct Python
python -m venv .venv

REM Install packages
.venv\Scripts\pip.exe install flask pandas numpy scikit-learn

echo.
echo ✅ FIXED! Now run: .venv\Scripts\python.exe app.py
pause
