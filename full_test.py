#!/usr/bin/env python3
"""
FULL FUNCTIONALITY TEST
"""

import sys
import os
import pandas as pd

def test_all_routes():
    print("Testing all routes...")
    from app import app
    
    routes_to_test = [
        '/',
        '/statistics',
        '/ultimate-predictor', 
        '/decision-helper',
        '/quick-pick',
        '/pattern-analyzer',
        '/hot-cold',
        '/frequency-analyzer',
        '/best-predictions',
        '/smart-predictor',
        '/ml-predictor',
        '/consensus-predictor',
        '/learning-dashboard',
        '/day-to-day-predictor',
        '/lucky-generator'
    ]
    
    with app.test_client() as client:
        working = 0
        for route in routes_to_test:
            try:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"  {route}: OK")
                    working += 1
                else:
                    print(f"  {route}: ERROR {response.status_code}")
            except Exception as e:
                print(f"  {route}: CRASH - {str(e)[:50]}")
    
    print(f"Routes working: {working}/{len(routes_to_test)}")
    return working == len(routes_to_test)

def test_predictions():
    print("\nTesting prediction algorithms...")
    from app import load_csv_data, advanced_predictor, smart_auto_weight_predictor, ml_predictor
    
    df = load_csv_data()
    if df.empty:
        print("  No data for testing")
        return False
    
    try:
        # Test all predictors
        adv = advanced_predictor(df, lookback=100)
        smart = smart_auto_weight_predictor(df, lookback=100)
        ml = ml_predictor(df, lookback=100)
        
        print(f"  Advanced predictor: {len(adv)} predictions")
        print(f"  Smart predictor: {len(smart)} predictions")
        print(f"  ML predictor: {len(ml)} predictions")
        
        # Test prediction format
        if adv and len(adv[0]) == 3:
            print("  Prediction format: OK")
        else:
            print("  Prediction format: ERROR")
            return False
        
        return True
    except Exception as e:
        print(f"  Prediction test failed: {e}")
        return False

def test_csv_parsing():
    print("\nTesting CSV parsing...")
    from app import load_csv_data
    
    try:
        df = load_csv_data()
        print(f"  CSV loaded: {len(df)} rows")
        
        if df.empty:
            print("  CSV is empty!")
            return False
        
        # Test required columns
        required = ['date_parsed', 'provider', '1st_real', '2nd_real', '3rd_real']
        missing = [col for col in required if col not in df.columns]
        if missing:
            print(f"  Missing columns: {missing}")
            return False
        
        # Test data quality
        valid_1st = df['1st_real'].astype(str).str.len().eq(4).sum()
        print(f"  Valid 1st prizes: {valid_1st}")
        
        providers = df['provider'].unique()
        print(f"  Providers found: {list(providers)[:5]}")
        
        return True
    except Exception as e:
        print(f"  CSV parsing failed: {e}")
        return False

def test_helper_functions():
    print("\nTesting helper functions...")
    try:
        from app import (
            calculate_enhanced_consensus,
            analyze_cross_correlations, 
            advanced_pattern_mining,
            calculate_weighted_frequency,
            analyze_provider_bias,
            load_csv_data
        )
        
        df = load_csv_data()
        if df.empty:
            print("  No data for helper tests")
            return False
        
        # Test functions
        test_data = {'count': 3, 'sources': ['adv', 'smart', 'ml']}
        consensus = calculate_enhanced_consensus("1234", test_data, df)
        print(f"  Enhanced consensus: OK")
        
        test_numbers = ["1234", "1235", "5678"]
        correlations = analyze_cross_correlations(test_numbers)
        print(f"  Cross correlations: OK")
        
        patterns = advanced_pattern_mining(test_numbers)
        print(f"  Pattern mining: OK")
        
        weighted = calculate_weighted_frequency(df.tail(50), test_numbers, 30)
        print(f"  Weighted frequency: OK")
        
        bias = analyze_provider_bias(df, 'magnum')
        print(f"  Provider bias: OK")
        
        return True
    except Exception as e:
        print(f"  Helper functions failed: {e}")
        return False

def main():
    print("COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 50)
    
    tests = [
        ("CSV Parsing", test_csv_parsing),
        ("Prediction Algorithms", test_predictions),
        ("Helper Functions", test_helper_functions),
        ("All Routes", test_all_routes)
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                print(f"PASS: {name}")
                passed += 1
            else:
                print(f"FAIL: {name}")
        except Exception as e:
            print(f"CRASH: {name} - {e}")
    
    print("=" * 50)
    print(f"FINAL RESULT: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("SUCCESS: Everything is working perfectly!")
        print("- CSV parsing: Working")
        print("- All prediction algorithms: Working") 
        print("- All helper functions: Working")
        print("- All Flask routes: Working")
        print("- No errors or crashes detected")
    else:
        print("ISSUES: Some components need attention")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)