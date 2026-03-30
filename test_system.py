# -*- coding: utf-8 -*-
"""
Test script to verify all routes are working
"""
import sys
sys.path.insert(0, '.')

print("=" * 80)
print("TESTING SMART 4D LOTTERY PREDICTION SYSTEM")
print("=" * 80)

# Test 1: Import app
print("\n[TEST 1] Importing app.py...")
try:
    import app
    print("[OK] SUCCESS: app.py imported without errors")
except Exception as e:
    print(f"[FAIL] {e}")
    sys.exit(1)

# Test 2: Check Flask app exists
print("\n[TEST 2] Checking Flask app...")
try:
    assert hasattr(app, 'app'), "Flask app not found"
    print("[OK] SUCCESS: Flask app exists")
except Exception as e:
    print(f"[FAIL] {e}")
    sys.exit(1)

# Test 3: Check key routes
print("\n[TEST 3] Checking key routes...")
routes_to_check = [
    '/decision-helper',
    '/pattern-analyzer',
    '/ultimate-predictor',
    '/past-results',
    '/smart-predictor',
    '/ml-predictor'
]

found_routes = []
for rule in app.app.url_map.iter_rules():
    found_routes.append(str(rule))

missing_routes = []
for route in routes_to_check:
    if route in found_routes:
        print(f"  [OK] {route}")
    else:
        print(f"  [FAIL] {route} - MISSING")
        missing_routes.append(route)

if missing_routes:
    print(f"\n[FAIL] {len(missing_routes)} routes missing")
    sys.exit(1)
else:
    print(f"\n[OK] All {len(routes_to_check)} key routes found")

# Test 4: Check prediction functions
print("\n[TEST 4] Checking prediction functions...")
functions_to_check = [
    'advanced_predictor',
    'smart_auto_weight_predictor',
    'ml_predictor',
    'load_csv_data'
]

for func_name in functions_to_check:
    if hasattr(app, func_name):
        print(f"  [OK] {func_name}()")
    else:
        print(f"  [FAIL] {func_name}() - MISSING")
        sys.exit(1)

print(f"\n[OK] All {len(functions_to_check)} functions found")

# Test 5: Check CSV data loading
print("\n[TEST 5] Testing CSV data loading...")
try:
    df = app.load_csv_data()
    print(f"  [OK] CSV loaded: {len(df)} rows")
    if len(df) > 0:
        print(f"  [OK] Data from {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
except Exception as e:
    print(f"  [FAIL] {e}")
    sys.exit(1)

# Final summary
print("\n" + "=" * 80)
print("[SUCCESS] ALL TESTS PASSED!")
print("=" * 80)
print("\nYour Smart 4D Lottery Prediction System is ready!")
print("\nTo start: python app.py")
print("Access: http://127.0.0.1:5000/decision-helper")
print("=" * 80)
