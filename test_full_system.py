import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'c:\Users\Acer\Desktop\smartsuraj')

print("="*60)
print("TESTING CSV PARSING AND PREDICTION LOGIC")
print("="*60)
print()

# Test 1: CSV Loading
print("TEST 1: CSV Loading")
print("-" * 60)
try:
    import pandas as pd
    df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')
    print(f"✓ CSV loaded: {len(df)} rows")
    print(f"✓ Columns: {list(df.columns)}")
    print(f"✓ First 3 rows:")
    for i in range(min(3, len(df))):
        row = df.iloc[i]
        print(f"  Row {i}: {row['date']} | {row['provider']} | 1st:{row['1st']} 2nd:{row['2nd']} 3rd:{row['3rd']}")
except Exception as e:
    print(f"✗ CSV error: {e}")
print()

# Test 2: App Load CSV Function
print("TEST 2: App load_csv_data() Function")
print("-" * 60)
try:
    from app import load_csv_data
    df = load_csv_data()
    print(f"✓ load_csv_data() works: {len(df)} rows")
    
    # Check required columns
    required_cols = ['date_parsed', 'provider', '1st_real', '2nd_real', '3rd_real']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"⚠ Missing columns: {missing}")
        print(f"  Available columns: {list(df.columns)}")
    else:
        print(f"✓ All required columns present")
        
    # Check data
    if len(df) > 0:
        print(f"✓ Sample data:")
        sample = df.iloc[0]
        for col in df.columns:
            print(f"  {col}: {sample[col]}")
            
except Exception as e:
    print(f"✗ Load error: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 3: Prediction Functions
print("TEST 3: Prediction Functions")
print("-" * 60)
try:
    from app import advanced_predictor, smart_auto_weight_predictor, ml_predictor
    
    df = load_csv_data()
    if len(df) > 0:
        # Test Advanced Predictor
        try:
            preds = advanced_predictor(df, provider='all', lookback=50)
            if preds:
                print(f"✓ Advanced Predictor: {len(preds)} predictions")
                for i, (num, score, reason) in enumerate(preds[:3]):
                    print(f"  {i+1}. {num} (score: {score:.2f}) - {reason}")
            else:
                print("⚠ Advanced Predictor returned empty")
        except Exception as e:
            print(f"✗ Advanced Predictor error: {e}")
        
        # Test Smart Predictor
        try:
            preds = smart_auto_weight_predictor(df, provider='all', lookback=50)
            if preds:
                print(f"✓ Smart Predictor: {len(preds)} predictions")
                for i, (num, score, reason) in enumerate(preds[:3]):
                    print(f"  {i+1}. {num} (score: {score:.2f}) - {reason}")
            else:
                print("⚠ Smart Predictor returned empty")
        except Exception as e:
            print(f"✗ Smart Predictor error: {e}")
        
        # Test ML Predictor
        try:
            preds = ml_predictor(df, lookback=50)
            if preds:
                print(f"✓ ML Predictor: {len(preds)} predictions")
                for i, (num, score, reason) in enumerate(preds[:3]):
                    print(f"  {i+1}. {num} (score: {score:.2f}) - {reason}")
            else:
                print("⚠ ML Predictor returned empty")
        except Exception as e:
            print(f"✗ ML Predictor error: {e}")
    else:
        print("✗ No data to test predictions")
        
except Exception as e:
    print(f"✗ Prediction test error: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 4: Pattern Analyzer
print("TEST 4: Pattern Analyzer (AI Predictor)")
print("-" * 60)
try:
    from utils.ai_predictor import predict_top_5
    from utils.app_grid import generate_4x4_grid
    
    test_number = "1234"
    grid = generate_4x4_grid(test_number)
    print(f"✓ Grid generated for {test_number}")
    
    result = predict_top_5([{'date': '2025-01-01', 'grid': grid, 'number': test_number}], mode="combined")
    if result and 'combined' in result:
        preds = result['combined']
        print(f"✓ AI Predictor: {len(preds)} predictions")
        for i, (num, score, reason) in enumerate(preds[:3]):
            print(f"  {i+1}. {num} (confidence: {score:.1f}%) - {reason}")
    else:
        print("⚠ AI Predictor returned empty")
        
except Exception as e:
    print(f"✗ AI Predictor error: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 5: Flask Routes
print("TEST 5: Flask App Routes")
print("-" * 60)
try:
    from app import app
    
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes.append(str(rule))
    
    print(f"✓ Flask app has {len(routes)} routes")
    print("  Key routes:")
    key_routes = ['/', '/pattern-analyzer', '/quick-pick', '/ultimate-predictor', '/statistics']
    for route in key_routes:
        if route in routes:
            print(f"    ✓ {route}")
        else:
            print(f"    ✗ {route} MISSING")
            
except Exception as e:
    print(f"✗ Flask routes error: {e}")
print()

print("="*60)
print("SUMMARY")
print("="*60)
print()
print("If you see ✓ marks above, the system is working!")
print()
print("To start the app:")
print("  1. Run: python app.py")
print("  2. Open: http://127.0.0.1:5000")
print()
print("="*60)
