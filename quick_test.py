#!/usr/bin/env python3
"""
QUICK TEST - Check core functionality
"""

import sys
import os
import pandas as pd

def test_csv():
    print("Testing CSV parsing...")
    try:
        df = pd.read_csv("4d_results_history.csv", on_bad_lines='skip')
        print(f"CSV loaded: {len(df)} rows")
        
        # Test date parsing
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        valid_dates = df['date_parsed'].notna().sum()
        print(f"Valid dates: {valid_dates}")
        
        # Test provider extraction
        df['provider_clean'] = df['provider'].str.extract(r'images/([^./\"]+)', expand=False)
        providers = df['provider_clean'].dropna().unique()
        print(f"Providers: {list(providers)[:3]}")
        
        return True
    except Exception as e:
        print(f"CSV test failed: {e}")
        return False

def test_app():
    print("\nTesting app import...")
    try:
        from app import app, load_csv_data, advanced_predictor
        print("App imported successfully")
        
        df = load_csv_data()
        print(f"Data loaded: {len(df)} rows")
        
        if not df.empty:
            preds = advanced_predictor(df, lookback=50)
            print(f"Predictions generated: {len(preds)}")
        
        return True
    except Exception as e:
        print(f"App test failed: {e}")
        return False

def test_routes():
    print("\nTesting Flask routes...")
    try:
        from app import app
        
        with app.test_client() as client:
            routes = ['/', '/statistics', '/ultimate-predictor', '/decision-helper']
            
            for route in routes:
                response = client.get(route)
                status = "OK" if response.status_code == 200 else f"ERROR {response.status_code}"
                print(f"{route}: {status}")
        
        return True
    except Exception as e:
        print(f"Routes test failed: {e}")
        return False

def main():
    print("SYSTEM TEST STARTING...")
    print("=" * 40)
    
    tests = [
        ("CSV Parsing", test_csv),
        ("App Import", test_app),
        ("Flask Routes", test_routes)
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
    
    print("=" * 40)
    print(f"RESULT: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("ALL SYSTEMS WORKING!")
    else:
        print("ISSUES DETECTED")

if __name__ == "__main__":
    main()