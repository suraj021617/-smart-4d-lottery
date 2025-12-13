@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting 4D Prediction System...
python simple_app.py

pause