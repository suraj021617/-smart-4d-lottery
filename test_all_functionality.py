"""
SMART 4D - COMPREHENSIVE FUNCTIONALITY TEST
Tests all routes, predictions, and logic
"""

import sys
import os

# Test imports
print("=" * 60)
print("TESTING IMPORTS")
print("=" * 60)

try:
    from flask import Flask
    print("[OK] Flask imported")
except ImportError as e:
    print(f"[FAIL] Flask import failed: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("[OK] Pandas imported")
except ImportError as e:
    print(f"[FAIL] Pandas import failed: {e}")
    sys.exit(1)

try:
    import numpy as np
    print("[OK] Numpy imported")
except ImportError as e:
    print(f"[FAIL] Numpy import failed: {e}")
    sys.exit(1)

try:
    from sklearn.linear_model import LinearRegression
    print("[OK] Scikit-learn imported")
except ImportError as e:
    print(f"[FAIL] Scikit-learn import failed: {e}")
    sys.exit(1)

# Import app
try:
    from app import app, load_csv_data, advanced_predictor, smart_auto_weight_predictor, ml_predictor
    print("[OK] App imported successfully")
except Exception as e:
    print(f"[FAIL] App import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TESTING DATA LOADING")
print("=" * 60)

try:
    df = load_csv_data()
    if df.empty:
        print("[WARN] CSV data is empty!")
    else:
        print(f"[OK] CSV loaded: {len(df)} rows")
        print(f"     Columns: {', '.join(df.columns[:5])}...")
        print(f"     Date range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")
        print(f"     Providers: {', '.join(df['provider_key'].unique()[:5])}")
except Exception as e:
    print(f"[FAIL] Data loading failed: {e}")
    df = pd.DataFrame()

print("\n" + "=" * 60)
print("TESTING ROUTES")
print("=" * 60)

routes = []
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        routes.append({
            'path': str(rule),
            'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
            'endpoint': rule.endpoint
        })

routes.sort(key=lambda x: x['path'])

print(f"Total routes found: {len(routes)}\n")

# Categorize routes
categories = {
    'Home & Main': [],
    'Predictions': [],
    'Analysis': [],
    'Statistics': [],
    'API & Export': [],
    'Other': []
}

for route in routes:
    path = route['path']
    if path in ['/', '/index']:
        categories['Home & Main'].append(route)
    elif any(word in path for word in ['predict', 'quick-pick', 'smart', 'ml', 'ultimate', 'best', 'consensus', 'super']):
        categories['Predictions'].append(route)
    elif any(word in path for word in ['pattern', 'analyzer', 'analysis', 'frequency', 'hot-cold']):
        categories['Analysis'].append(route)
    elif any(word in path for word in ['statistics', 'history', 'results', 'accuracy', 'learning']):
        categories['Statistics'].append(route)
    elif any(word in path for word in ['api', 'export', 'save', 'evaluate']):
        categories['API & Export'].append(route)
    else:
        categories['Other'].append(route)

for category, items in categories.items():
    if items:
        print(f"\n{category} ({len(items)} routes):")
        for item in items:
            print(f"  [OK] {item['path']:<40} [{item['methods']}]")

print("\n" + "=" * 60)
print("TESTING PREDICTION FUNCTIONS")
print("=" * 60)

prediction_results = {
    'advanced': False,
    'smart': False,
    'ml': False
}

if not df.empty:
    # Test Advanced Predictor
    try:
        adv_preds = advanced_predictor(df, provider='all', lookback=50)
        if adv_preds:
            print(f"[OK] Advanced Predictor: {len(adv_preds)} predictions")
            print(f"     Top prediction: {adv_preds[0][0]} (score: {adv_preds[0][1]:.3f})")
            prediction_results['advanced'] = True
        else:
            print("[WARN] Advanced Predictor: No predictions generated")
    except Exception as e:
        print(f"[FAIL] Advanced Predictor failed: {e}")

    # Test Smart Predictor
    try:
        smart_preds = smart_auto_weight_predictor(df, provider='all', lookback=50)
        if smart_preds:
            print(f"[OK] Smart Predictor: {len(smart_preds)} predictions")
            print(f"     Top prediction: {smart_preds[0][0]} (score: {smart_preds[0][1]:.3f})")
            prediction_results['smart'] = True
        else:
            print("[WARN] Smart Predictor: No predictions generated")
    except Exception as e:
        print(f"[FAIL] Smart Predictor failed: {e}")

    # Test ML Predictor
    try:
        ml_preds = ml_predictor(df, lookback=50)
        if ml_preds:
            print(f"[OK] ML Predictor: {len(ml_preds)} predictions")
            print(f"     Top prediction: {ml_preds[0][0]} (score: {ml_preds[0][1]:.3f})")
            prediction_results['ml'] = True
        else:
            print("[WARN] ML Predictor: No predictions generated")
    except Exception as e:
        print(f"[FAIL] ML Predictor failed: {e}")
else:
    print("[WARN] Skipping prediction tests - no data loaded")

print("\n" + "=" * 60)
print("TESTING CRITICAL ROUTES")
print("=" * 60)

route_results = {}

with app.test_client() as client:
    critical_routes = [
        ('/', 'Home Page'),
        ('/quick-pick', 'Quick Pick'),
        ('/pattern-analyzer', 'Pattern Analyzer'),
        ('/ultimate-predictor', 'Ultimate Predictor'),
        ('/smart-predictor', 'Smart Predictor'),
        ('/ml-predictor', 'ML Predictor'),
        ('/statistics', 'Statistics'),
        ('/past-results', 'Past Results'),
        ('/hot-cold', 'Hot Cold Numbers'),
        ('/frequency-analyzer', 'Frequency Analyzer'),
        ('/day-to-day-predictor', 'Day to Day Predictor'),
        ('/best-predictions', 'Best Predictions'),
        ('/accuracy-dashboard', 'Accuracy Dashboard'),
    ]
    
    for route, name in critical_routes:
        try:
            response = client.get(route)
            if response.status_code == 200:
                print(f"[OK] {name:<30} - Status: {response.status_code}")
                route_results[route] = True
            elif response.status_code == 302:
                print(f"[WARN] {name:<30} - Redirect: {response.status_code}")
                route_results[route] = True
            else:
                print(f"[FAIL] {name:<30} - Error: {response.status_code}")
                route_results[route] = False
        except Exception as e:
            print(f"[FAIL] {name:<30} - Exception: {str(e)[:50]}")
            route_results[route] = False

print("\n" + "=" * 60)
print("TESTING UTILITY FUNCTIONS")
print("=" * 60)

utils_working = 0
utils_total = 0

try:
    from utils.app_grid import generate_4x4_grid, generate_reverse_grid
    grid = generate_4x4_grid("1234")
    print(f"[OK] Grid generation works: {len(grid)}x{len(grid[0])} grid")
    utils_working += 1
except Exception as e:
    print(f"[FAIL] Grid generation failed: {e}")
utils_total += 1

try:
    from utils.data_normalizer import normalize_dataframe
    print("[OK] Data normalizer imported")
    utils_working += 1
except Exception as e:
    print(f"[FAIL] Data normalizer failed: {e}")
utils_total += 1

try:
    from utils.pattern_finder import find_all_4digit_patterns
    print("[OK] Pattern finder imported")
    utils_working += 1
except Exception as e:
    print(f"[FAIL] Pattern finder failed: {e}")
utils_total += 1

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

working_routes = sum(1 for v in route_results.values() if v)
total_routes = len(route_results)
working_predictions = sum(1 for v in prediction_results.values() if v)
total_predictions = len(prediction_results)

print(f"""
RESULTS:
  Total Routes: {len(routes)}
  Critical Routes Working: {working_routes}/{total_routes}
  Prediction Functions Working: {working_predictions}/{total_predictions}
  Utility Functions Working: {utils_working}/{utils_total}
  Data Rows Loaded: {len(df) if not df.empty else 0}

PREDICTION STATUS:
  Advanced Predictor: {'[OK]' if prediction_results['advanced'] else '[FAIL]'}
  Smart Predictor: {'[OK]' if prediction_results['smart'] else '[FAIL]'}
  ML Predictor: {'[OK]' if prediction_results['ml'] else '[FAIL]'}

CRITICAL ROUTES STATUS:
""")

for route, status in route_results.items():
    print(f"  {route:<30} {'[OK]' if status else '[FAIL]'}")

if working_routes == total_routes and working_predictions == total_predictions:
    print("\n[SUCCESS] All systems operational!")
    print("\nTO START THE APP:")
    print("  python app.py")
    print("\nTHEN OPEN:")
    print("  http://127.0.0.1:5000")
else:
    print("\n[WARNING] Some issues detected. Check the output above.")
    if working_predictions < total_predictions:
        print("  - Some prediction functions failed")
    if working_routes < total_routes:
        print("  - Some routes are not working")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
