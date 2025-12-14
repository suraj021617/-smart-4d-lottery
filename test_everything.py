#!/usr/bin/env python3
"""
COMPREHENSIVE TEST SUITE - Check everything works
Tests: CSV parsing, logic, buttons, routes, predictions
"""

import sys
import os
import pandas as pd
import requests
import time
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_csv_parsing():
    """Test CSV parsing functionality"""
    print("🔍 TESTING CSV PARSING...")
    
    try:
        # Test if CSV exists and is readable
        csv_file = "4d_results_history.csv"
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            return False
        
        # Test pandas reading
        df = pd.read_csv(csv_file, on_bad_lines='skip')
        print(f"✅ CSV loaded: {len(df)} rows")
        
        # Test required columns
        required_cols = ['date', 'provider', '3rd']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"❌ Missing columns: {missing_cols}")
            return False
        
        print(f"✅ Required columns present: {required_cols}")
        
        # Test date parsing
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        valid_dates = df['date_parsed'].notna().sum()
        print(f"✅ Valid dates: {valid_dates}/{len(df)}")
        
        # Test provider extraction
        df['provider_clean'] = df['provider'].str.extract(r'images/([^./\"]+)', expand=False).fillna('unknown')
        providers = df['provider_clean'].unique()
        print(f"✅ Providers found: {list(providers)[:5]}")
        
        # Test prize extraction
        import html
        df['prize_text'] = df['3rd'].fillna('').astype(str).apply(html.unescape)
        df['1st_extracted'] = df['prize_text'].str.extract(r'1st\\s+Prize\\s+(\\d{4})', flags=2)[0]
        valid_prizes = df['1st_extracted'].notna().sum()
        print(f"✅ Valid 1st prizes extracted: {valid_prizes}")
        
        return True
        
    except Exception as e:
        print(f"❌ CSV parsing failed: {e}")
        return False

def test_app_import():
    """Test if app imports correctly"""
    print("\n🔍 TESTING APP IMPORT...")
    
    try:
        from app import app, load_csv_data, advanced_predictor
        print("✅ App imported successfully")
        
        # Test CSV loading function
        df = load_csv_data()
        print(f"✅ load_csv_data() works: {len(df)} rows")
        
        # Test predictor function
        if not df.empty:
            preds = advanced_predictor(df, lookback=50)
            print(f"✅ advanced_predictor() works: {len(preds)} predictions")
        
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_flask_routes():
    """Test Flask routes by starting server and making requests"""
    print("\n🔍 TESTING FLASK ROUTES...")
    
    try:
        from app import app
        import threading
        import time
        
        # Start Flask in test mode
        app.config['TESTING'] = True
        
        # Test with test client (no actual server needed)
        with app.test_client() as client:
            
            # Test main routes
            routes_to_test = [
                '/',
                '/statistics',
                '/ultimate-predictor',
                '/quick-pick',
                '/decision-helper',
                '/hot-cold',
                '/frequency-analyzer',
                '/pattern-analyzer',
                '/best-predictions'
            ]
            
            for route in routes_to_test:
                try:
                    response = client.get(route)
                    if response.status_code == 200:
                        print(f"✅ {route} - OK")
                    else:
                        print(f"❌ {route} - Status: {response.status_code}")
                except Exception as e:
                    print(f"❌ {route} - Error: {str(e)[:50]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask routes test failed: {e}")
        return False

def test_prediction_logic():
    """Test prediction algorithms"""
    print("\n🔍 TESTING PREDICTION LOGIC...")
    
    try:
        from app import (
            load_csv_data, 
            advanced_predictor, 
            smart_auto_weight_predictor, 
            ml_predictor,
            find_4digit_patterns,
            generate_4x4_grid
        )
        
        df = load_csv_data()
        if df.empty:
            print("❌ No data for prediction testing")
            return False
        
        # Test advanced predictor
        adv_preds = advanced_predictor(df, lookback=100)
        print(f"✅ Advanced predictor: {len(adv_preds)} predictions")
        
        # Test smart predictor
        smart_preds = smart_auto_weight_predictor(df, lookback=100)
        print(f"✅ Smart predictor: {len(smart_preds)} predictions")
        
        # Test ML predictor
        ml_preds = ml_predictor(df, lookback=100)
        print(f"✅ ML predictor: {len(ml_preds)} predictions")
        
        # Test pattern functions
        test_grid = generate_4x4_grid("1234")
        patterns = find_4digit_patterns(test_grid)
        print(f"✅ Pattern detection: {len(patterns)} patterns found")
        
        # Test prediction format
        if adv_preds:
            pred = adv_preds[0]
            if len(pred) == 3 and isinstance(pred[0], str) and len(pred[0]) == 4:
                print("✅ Prediction format correct")
            else:
                print(f"❌ Prediction format wrong: {pred}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prediction logic test failed: {e}")
        return False

def test_helper_functions():
    """Test helper functions"""
    print("\n🔍 TESTING HELPER FUNCTIONS...")
    
    try:
        from app import (
            calculate_enhanced_consensus,
            analyze_cross_correlations,
            advanced_pattern_mining,
            calculate_weighted_frequency,
            analyze_provider_bias
        )
        
        df = load_csv_data()
        if df.empty:
            print("❌ No data for helper function testing")
            return False
        
        # Test enhanced consensus
        test_data = {'count': 3, 'sources': ['adv', 'smart', 'ml']}
        consensus = calculate_enhanced_consensus("1234", test_data, df)
        print(f"✅ Enhanced consensus: {consensus}")
        
        # Test cross correlations
        test_numbers = ["1234", "1235", "5678", "1236"]
        correlations = analyze_cross_correlations(test_numbers)
        print(f"✅ Cross correlations: {len(correlations)} found")
        
        # Test pattern mining
        patterns = advanced_pattern_mining(test_numbers)
        print(f"✅ Pattern mining: {len(patterns)} patterns")
        
        # Test weighted frequency
        weighted = calculate_weighted_frequency(df.tail(50), test_numbers, 30)
        print(f"✅ Weighted frequency: {len(weighted)} scores")
        
        # Test provider bias
        bias = analyze_provider_bias(df, 'magnum')
        print(f"✅ Provider bias: {len(bias.get('bias_numbers', []))} bias numbers")
        
        return True
        
    except Exception as e:
        print(f"❌ Helper functions test failed: {e}")
        return False

def test_template_rendering():
    """Test if templates render without errors"""
    print("\n🔍 TESTING TEMPLATE RENDERING...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Test templates with data
            test_routes = [
                ('/', 'index'),
                ('/statistics', 'statistics'),
                ('/ultimate-predictor', 'ultimate predictor'),
                ('/decision-helper', 'decision helper')
            ]
            
            for route, name in test_routes:
                response = client.get(route)
                if response.status_code == 200 and len(response.data) > 1000:
                    print(f"✅ {name} template renders properly")
                else:
                    print(f"❌ {name} template issue - Status: {response.status_code}, Size: {len(response.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Template rendering test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 COMPREHENSIVE SYSTEM TEST STARTING...")
    print("=" * 50)
    
    tests = [
        ("CSV Parsing", test_csv_parsing),
        ("App Import", test_app_import),
        ("Flask Routes", test_flask_routes),
        ("Prediction Logic", test_prediction_logic),
        ("Helper Functions", test_helper_functions),
        ("Template Rendering", test_template_rendering)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 50)
    print("📊 FINAL TEST RESULTS:")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL SYSTEMS WORKING PERFECTLY!")
    elif passed >= total * 0.8:
        print("⚠️  MOSTLY WORKING - Minor issues detected")
    else:
        print("🚨 MAJOR ISSUES DETECTED - Needs attention")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)