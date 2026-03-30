#!/usr/bin/env python
"""
COMPREHENSIVE PROJECT TEST - Check ALL routes, buttons, logic
"""

import sys
import traceback
from app import app, load_csv_data
from utils.app_grid import generate_4x4_grid, generate_reverse_grid
from utils.pattern_finder import find_all_4digit_patterns
from utils.ai_predictor import predict_top_5

print("="*80)
print("SMART 4D LOTTERY - COMPREHENSIVE SYSTEM TEST")
print("="*80)

# Test 1: Data Loading
print("\n[TEST 1] DATA LOADING")
print("-"*80)
try:
    df = load_csv_data()
    if df.empty:
        print("❌ FAIL: CSV data is empty")
    else:
        print(f"[PASS] Loaded {len(df)} rows")
        print(f"   Columns: {list(df.columns)[:8]}")
        print(f"   Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
except Exception as e:
    print(f"[FAIL] {e}")

# Test 2: Grid Generation
print("\n[TEST 2] GRID GENERATION")
print("-"*80)
test_numbers = ["1234", "5678", "0000", "9999"]
for num in test_numbers:
    try:
        grid = generate_4x4_grid(num)
        reverse = generate_reverse_grid(num)
        if len(grid) == 4 and len(reverse) == 4:
            print(f"✅ PASS: {num} -> Grid OK, Reverse OK")
        else:
            print(f"❌ FAIL: {num} -> Invalid grid size")
    except Exception as e:
        print(f"❌ FAIL: {num} -> {e}")

# Test 3: Pattern Finding
print("\n[TEST 3] PATTERN FINDING")
print("-"*80)
try:
    grid = generate_4x4_grid("1234")
    patterns = find_all_4digit_patterns(grid)
    if len(patterns) > 0:
        print(f"✅ PASS: Found {len(patterns)} patterns")
        unique = list(set([p for _, _, p, _ in patterns]))
        print(f"   Unique 4D numbers: {len(unique)}")
        print(f"   Sample: {unique[:5]}")
    else:
        print("❌ FAIL: No patterns found")
except Exception as e:
    print(f"❌ FAIL: {e}")

# Test 4: AI Predictions
print("\n[TEST 4] AI PREDICTIONS")
print("-"*80)
try:
    grid = generate_4x4_grid("1234")
    draw_data = [{'date': '2025-01-01', 'grid': grid}]
    
    for mode in ['pattern', 'combined']:
        preds = predict_top_5(draw_data, mode=mode)
        if isinstance(preds, dict) and len(preds.get('combined', [])) > 0:
            print(f"✅ PASS: Mode '{mode}' -> {len(preds.get('combined', []))} predictions")
        else:
            print(f"❌ FAIL: Mode '{mode}' -> No predictions")
except Exception as e:
    print(f"❌ FAIL: {e}")

# Test 5: All Routes
print("\n[TEST 5] ROUTE AVAILABILITY")
print("-"*80)

routes_to_test = [
    ('/', 'Home/Index'),
    ('/pattern-analyzer', 'Pattern Analyzer'),
    ('/best-predictions', 'Best Predictions'),
    ('/smart-predictor', 'Smart Predictor'),
    ('/ml-predictor', 'ML Predictor'),
    ('/ultimate-predictor', 'Ultimate Predictor'),
    ('/quick-pick', 'Quick Pick'),
    ('/day-to-day-predictor', 'Day-to-Day Predictor'),
    ('/statistics', 'Statistics'),
    ('/hot-cold', 'Hot/Cold Numbers'),
    ('/frequency-analyzer', 'Frequency Analyzer'),
    ('/empty-box-predictor', 'Empty Box Predictor'),
    ('/lucky-generator', 'Lucky Generator'),
    ('/accuracy-dashboard', 'Accuracy Dashboard'),
    ('/learning-insights', 'Learning Insights'),
    ('/past-results', 'Past Results'),
    ('/decision-helper', 'Decision Helper'),
    ('/consensus-predictor', 'Consensus Predictor'),
    ('/best-pick', 'Best Pick'),
]

with app.test_client() as client:
    for route, name in routes_to_test:
        try:
            response = client.get(route)
            if response.status_code == 200:
                print(f"✅ PASS: {name:30s} ({route})")
            elif response.status_code == 302:
                print(f"⚠️  REDIRECT: {name:30s} ({route}) -> {response.location}")
            else:
                print(f"❌ FAIL: {name:30s} ({route}) -> Status {response.status_code}")
        except Exception as e:
            print(f"❌ ERROR: {name:30s} ({route}) -> {str(e)[:50]}")

# Test 6: Predictor Functions
print("\n[TEST 6] PREDICTOR FUNCTIONS")
print("-"*80)

from app import advanced_predictor, smart_auto_weight_predictor, ml_predictor

try:
    df = load_csv_data()
    if not df.empty:
        # Test Advanced Predictor
        try:
            adv = advanced_predictor(df.tail(100), provider='all', lookback=50)
            if adv and len(adv) > 0:
                print(f"✅ PASS: Advanced Predictor -> {len(adv)} predictions")
            else:
                print("❌ FAIL: Advanced Predictor -> No predictions")
        except Exception as e:
            print(f"❌ FAIL: Advanced Predictor -> {str(e)[:60]}")
        
        # Test Smart Predictor
        try:
            smart = smart_auto_weight_predictor(df.tail(100), provider='all', lookback=50)
            if smart and len(smart) > 0:
                print(f"✅ PASS: Smart Predictor -> {len(smart)} predictions")
            else:
                print("❌ FAIL: Smart Predictor -> No predictions")
        except Exception as e:
            print(f"❌ FAIL: Smart Predictor -> {str(e)[:60]}")
        
        # Test ML Predictor
        try:
            ml = ml_predictor(df.tail(100), lookback=50)
            if ml and len(ml) > 0:
                print(f"✅ PASS: ML Predictor -> {len(ml)} predictions")
            else:
                print("❌ FAIL: ML Predictor -> No predictions")
        except Exception as e:
            print(f"❌ FAIL: ML Predictor -> {str(e)[:60]}")
except Exception as e:
    print(f"❌ FAIL: Could not test predictors -> {e}")

# Test 7: Template Files
print("\n[TEST 7] TEMPLATE FILES")
print("-"*80)

import os
template_dir = 'templates'
required_templates = [
    'index_clean.html',
    'pattern_analyzer.html',
    'best_predictions.html',
    'smart_predictor.html',
    'ml_predictor.html',
    'ultimate_predictor.html',
    'quick_pick.html',
    'statistics.html',
    'past_results.html',
]

for template in required_templates:
    path = os.path.join(template_dir, template)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ PASS: {template:30s} ({size:,} bytes)")
    else:
        print(f"❌ FAIL: {template:30s} (NOT FOUND)")

# Test 8: Utils Modules
print("\n[TEST 8] UTILS MODULES")
print("-"*80)

utils_modules = [
    'utils.app_grid',
    'utils.pattern_finder',
    'utils.ai_predictor',
    'utils.data_normalizer',
    'utils.pattern_stats',
    'utils.pattern_memory',
    'utils.pattern_predictor',
]

for module in utils_modules:
    try:
        __import__(module)
        print(f"✅ PASS: {module}")
    except ImportError as e:
        print(f"❌ FAIL: {module} -> {str(e)[:50]}")

# Test 9: Data Integrity
print("\n[TEST 9] DATA INTEGRITY")
print("-"*80)

try:
    df = load_csv_data()
    
    # Check for required columns
    required_cols = ['date_parsed', 'provider_key', 'number_1st', 'number_2nd', 'number_3rd']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"❌ FAIL: Missing columns: {missing_cols}")
    else:
        print(f"✅ PASS: All required columns present")
    
    # Check for valid 4D numbers
    valid_1st = df['number_1st'].astype(str).str.match(r'^\d{4}$').sum()
    total_1st = len(df)
    
    if valid_1st > 0:
        print(f"✅ PASS: Valid 4D numbers: {valid_1st}/{total_1st} ({valid_1st/total_1st*100:.1f}%)")
    else:
        print(f"❌ FAIL: No valid 4D numbers found")
    
    # Check date range
    if not df['date_parsed'].isna().all():
        print(f"✅ PASS: Date range valid")
    else:
        print(f"❌ FAIL: All dates are NaN")
        
except Exception as e:
    print(f"❌ FAIL: Data integrity check failed -> {e}")

# Test 10: Performance Check
print("\n[TEST 10] PERFORMANCE CHECK")
print("-"*80)

import time

try:
    # Test grid generation speed
    start = time.time()
    for i in range(100):
        generate_4x4_grid(f"{i:04d}")
    grid_time = time.time() - start
    print(f"✅ Grid generation: {grid_time:.3f}s for 100 numbers ({grid_time*10:.1f}ms each)")
    
    # Test pattern finding speed
    grid = generate_4x4_grid("1234")
    start = time.time()
    for i in range(10):
        find_all_4digit_patterns(grid)
    pattern_time = time.time() - start
    print(f"✅ Pattern finding: {pattern_time:.3f}s for 10 grids ({pattern_time*100:.1f}ms each)")
    
except Exception as e:
    print(f"❌ FAIL: Performance test failed -> {e}")

# FINAL SUMMARY
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)
print("Review the results above to identify any failing components.")
print("All ✅ PASS = System working correctly")
print("Any ❌ FAIL = Needs attention")
print("="*80)
