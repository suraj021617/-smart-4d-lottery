@echo off
echo Installing code formatter...
pip install black autopep8 -q

echo.
echo Formatting app.py...
black app.py --line-length 120 --quiet

echo.
echo DONE! Formatting complete.
pause
