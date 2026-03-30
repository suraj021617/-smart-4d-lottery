@echo off
echo ========================================
echo  SAFE CSV NORMALIZATION - PHASE 1
echo ========================================
echo.
echo This will create a NEW normalized CSV file.
echo Your original CSV will NOT be touched!
echo.
pause

python normalize_csv.py

echo.
echo ========================================
echo  DONE!
echo ========================================
echo.
echo Next steps:
echo 1. Check if 4d_results_normalized.csv was created
echo 2. Read MIGRATION_GUIDE.md for next steps
echo.
pause
