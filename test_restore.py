import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Testing restored project...")
print()

# Test 1: CSV loads
try:
    import pandas as pd
    df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')
    print(f"✓ CSV loads: {len(df)} rows")
except Exception as e:
    print(f"✗ CSV error: {e}")

# Test 2: App imports
try:
    from app import app, load_csv_data
    print("✓ App imports successfully")
except Exception as e:
    print(f"✗ App import error: {e}")

# Test 3: Load data
try:
    df = load_csv_data()
    print(f"✓ load_csv_data() works: {len(df)} rows")
    if len(df) > 0:
        print(f"✓ Latest date: {df['date_parsed'].max()}")
        print(f"✓ Providers: {df['provider_key'].nunique()}")
except Exception as e:
    print(f"✗ Load data error: {e}")

print()
print("=" * 50)
print("If you see ✓ marks above, the restore worked!")
print("Now run: START_APP_NOW.bat")
print("=" * 50)
