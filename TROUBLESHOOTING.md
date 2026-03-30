# 🔧 TROUBLESHOOTING GUIDE

## Common Issues and Solutions

---

## 1. Installation Issues

### Problem: `pip install` fails
**Solution:**
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt

# Or install individually
pip install flask pandas numpy scikit-learn
```

### Problem: Module not found error
**Solution:**
```bash
# Make sure you're in the correct directory
cd c:\Users\Acer\Desktop\smartsuraj

# Verify utils folder exists
dir utils

# Run from project root
python app.py
```

---

## 2. Data Loading Issues

### Problem: CSV file not found
**Solution:**
```python
# Check file exists
# File should be: 4d_results_history.csv
# In same directory as app.py

# If file has different name, update in app.py:
_history_df = load_history_data('your_file_name.csv')
```

### Problem: CSV parsing errors
**Solution:**
```python
# Check CSV format
# Should have columns: date, provider, number, draw_no
# Dates should be parseable (YYYY-MM-DD format)

# If format is different, update history_loader.py
# extract_4d_numbers_from_row() function
```

### Problem: No data loaded
**Solution:**
```bash
# Check console output when starting app
# Should show: "✓ Loaded X records"

# If 0 records, check CSV format
# Make sure numbers are extractable
```

---

## 3. Prediction Issues

### Problem: No predictions generated
**Solution:**
```python
# Check if sufficient historical data exists
# Need at least 100 records before target date

# Check console for error messages
# May show "Insufficient data" error

# Try selecting an earlier date
# Or add more historical data to CSV
```

### Problem: All predictions are the same
**Solution:**
```python
# This is normal if:
# - Very limited data
# - All predictors agree strongly

# To get more variety:
# - Add more historical data
# - Try different time windows
# - Check if weights are too similar
```

### Problem: Predictions seem random
**Solution:**
```python
# This can happen if:
# - Not enough evaluations yet
# - Weights not tuned
# - Data has no clear patterns

# Solution:
# - Run more evaluation cycles
# - System will learn over time
# - Check drift analysis for pattern changes
```

---

## 4. Evaluation Issues

### Problem: Log ID not found
**Solution:**
```bash
# Check prediction_logs.jsonl exists
# Should be created after first prediction

# Log ID format: YYYYMMDD_provider
# Example: 20250924_all

# Make sure you copied the correct log ID
# It's shown after making a prediction
```

### Problem: Evaluation doesn't update weights
**Solution:**
```python
# Check evaluation_logs.jsonl is being created
# Weights update after evaluation completes

# Check model_weights.json for changes
# Should update after each evaluation

# If not updating:
# - Check file permissions
# - Check for error messages in console
```

### Problem: Match scores seem wrong
**Solution:**
```python
# Match score is positional (0-4)
# 4 = exact match
# 3 = 3 digits in correct position
# 2 = 2 digits in correct position
# 1 = 1 digit in correct position
# 0 = no positional matches

# Example:
# Predicted: 1234
# Actual: 1256
# Score: 2 (first two digits match)
```

---

## 5. Performance Issues

### Problem: App is slow to start
**Solution:**
```python
# First load is slower (loading CSV)
# Subsequent loads use cache

# To speed up:
# 1. Reduce default window to 3 years
# 2. Use smaller CSV for testing
# 3. Increase cache efficiency

# In active_data_filter.py:
# Change default from 5 years to 3 years
```

### Problem: Predictions take too long
**Solution:**
```python
# If using "ALL (Consensus)":
# - Runs all 7 predictors
# - Takes longer but more accurate

# For faster predictions:
# - Use individual predictors
# - Use "Last 5 Years" (fastest)
# - Avoid "Full History" (slowest)
```

### Problem: Memory issues with large CSV
**Solution:**
```python
# If CSV is very large (100k+ records):
# 1. Use only recent data
# 2. Split CSV by year
# 3. Increase system RAM

# In history_loader.py:
# Add row limit:
# df = df.tail(50000)  # Keep last 50k records
```

---

## 6. UI Issues

### Problem: Buttons don't work
**Solution:**
```javascript
// Check browser console for errors (F12)
// Common issues:
// - JavaScript errors
// - API endpoint not responding
// - CORS issues

// Try:
// 1. Hard refresh (Ctrl+F5)
// 2. Clear browser cache
// 3. Check Flask is running
```

### Problem: Predictions don't display
**Solution:**
```javascript
// Check:
// 1. API response in browser console
// 2. Flask console for errors
// 3. JSON format is correct

// Try:
// - Refresh page
// - Check network tab in browser
// - Verify API endpoint returns data
```

### Problem: Date picker issues
**Solution:**
```javascript
// If date picker doesn't work:
// 1. Use Today/Tomorrow buttons
// 2. Manually type date in YYYY-MM-DD format
// 3. Check browser compatibility
```

---

## 7. API Issues

### Problem: 404 errors
**Solution:**
```python
# Check Flask is running on correct port
# Default: http://127.0.0.1:5000

# If port is in use:
# Change in app.py:
# app.run(debug=True, port=5001)
```

### Problem: 500 errors
**Solution:**
```python
# Check Flask console for error details
# Common causes:
# - Missing data
# - Invalid date format
# - File permission issues

# Enable debug mode in app.py:
# app.run(debug=True)
```

### Problem: CORS errors
**Solution:**
```python
# If accessing from different domain:
# Install flask-cors:
# pip install flask-cors

# Add to app.py:
# from flask_cors import CORS
# CORS(app)
```

---

## 8. File Issues

### Problem: Can't write to log files
**Solution:**
```bash
# Check file permissions
# Files should be writable:
# - prediction_logs.jsonl
# - evaluation_logs.jsonl
# - model_weights.json

# On Windows:
# Right-click → Properties → Security
# Make sure you have write permissions
```

### Problem: Log files corrupted
**Solution:**
```bash
# Backup and delete corrupted files:
# - prediction_logs.jsonl
# - evaluation_logs.jsonl

# System will create new files
# Previous data will be lost
```

### Problem: Cache not invalidating
**Solution:**
```python
# Force clear cache:
# In Python console or add to app.py:

from utils.history_loader import clear_cache
clear_cache()

# Or restart the app
```

---

## 9. Weight Issues

### Problem: Weights not changing
**Solution:**
```python
# Weights update slowly (learning_rate = 0.1)
# Need multiple evaluations to see change

# To speed up learning:
# In weight_updater.py:
# update_weights_after_result(learning_rate=0.3)

# Or reset weights:
from utils.weight_updater import reset_weights_to_default
reset_weights_to_default()
```

### Problem: Weights seem wrong
**Solution:**
```python
# Check current weights:
# GET /api/weights

# Weights range: 0.3 to 2.0
# Default: ~1.0
# Higher = better recent performance

# If weights are extreme:
# - Reset to default
# - Check evaluation data
# - Verify match scores are correct
```

---

## 10. Data Quality Issues

### Problem: Duplicate numbers in predictions
**Solution:**
```python
# System should remove duplicates
# If seeing duplicates:
# - Check consensus.py
# - Verify deduplication logic
# - May be bug in specific predictor

# Quick fix in prediction_runner.py:
# Add extra deduplication step
```

### Problem: Invalid 4D numbers
**Solution:**
```python
# All numbers should be 0000-9999
# If seeing invalid numbers:
# - Check normalize_to_4d() function
# - Verify CSV data quality
# - Add validation in predictors
```

### Problem: Historical data seems wrong
**Solution:**
```python
# Verify CSV data:
# - Check dates are correct
# - Check numbers are 4 digits
# - Check no future dates

# Use history match to verify:
# Enter known winning number
# Check if it appears on correct date
```

---

## 11. Learning Issues

### Problem: System not improving
**Solution:**
```python
# Learning requires:
# 1. Multiple prediction cycles
# 2. Evaluations after each result
# 3. Time for weights to adapt

# Check:
# - Are you evaluating regularly?
# - Check leaderboard for performance
# - Need at least 10-20 evaluations

# If still not improving:
# - Data may have no patterns
# - Try different time windows
# - Check drift analysis
```

### Problem: Performance getting worse
**Solution:**
```python
# Possible causes:
# 1. Recent pattern shift (drift)
# 2. Overfitting to old patterns
# 3. Bad evaluation data

# Solutions:
# - Check drift analysis
# - Reset weights to default
# - Use shorter time window
# - Verify evaluation data is correct
```

---

## 12. Debug Mode

### Enable Detailed Logging
```python
# In app.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)

# Or add print statements in modules:
print(f"Debug: {variable_name}")
```

### Check System Status
```python
# In Python console:
from utils.history_loader import load_history_data
df = load_history_data()
print(f"Records: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

from utils.consensus import get_current_weights
print(f"Weights: {get_current_weights()}")
```

---

## 13. Reset Everything

### Complete Reset
```bash
# 1. Stop the app (Ctrl+C)

# 2. Delete generated files:
del model_weights.json
del prediction_logs.jsonl
del evaluation_logs.jsonl

# 3. Clear Python cache:
del /s /q __pycache__
del /s /q utils\__pycache__

# 4. Restart app:
python app.py
```

---

## 14. Getting Help

### Check Documentation
1. README_REFACTORED.md - Full documentation
2. QUICKSTART.md - Quick start guide
3. ARCHITECTURE.md - System design
4. This file - Troubleshooting

### Check Code Comments
- All modules have extensive comments
- Read function docstrings
- Check inline comments

### Debug Steps
1. Check Flask console for errors
2. Check browser console (F12)
3. Enable debug mode
4. Add print statements
5. Test with simple data

---

## 15. Contact & Support

### Self-Help
- Read all documentation files
- Check code comments
- Use debug mode
- Test with minimal data

### Common Solutions
- Restart the app
- Clear cache
- Reset weights
- Verify data format
- Check file permissions

---

**🔧 Most issues can be solved by:**
1. Restarting the app
2. Checking console output
3. Verifying data format
4. Reading error messages carefully
5. Following this guide

**Good luck! 🎯**
