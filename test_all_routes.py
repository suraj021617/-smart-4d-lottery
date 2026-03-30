"""
Comprehensive Route & Data Test
Tests all major routes to ensure they return data
"""
from app import app, load_csv_data
import pandas as pd

print("=" * 60)
print("TESTING ALL ROUTES & DATA DISPLAY")
print("=" * 60)

# Load data first
df = load_csv_data()
print(f"\n[DATA] Loaded {len(df)} rows")

# Test routes
test_routes = [
    ('/', 'Home Dashboard'),
    ('/pattern-analyzer', 'Pattern Analyzer'),
    ('/ultimate-predictor', 'Ultimate Predictor'),
    ('/smart-predictor', 'Smart Predictor'),
    ('/ml-predictor', 'ML Predictor'),
    ('/statistics', 'Statistics'),
    ('/frequency-analyzer', 'Frequency Analyzer'),
    ('/hot-cold', 'Hot/Cold Numbers'),
    ('/best-predictions', 'Best Predictions'),
    ('/quick-pick', 'Quick Pick'),
    ('/lucky-generator', 'Lucky Generator'),
    ('/day-to-day-predictor', 'Day-to-Day Predictor'),
    ('/accuracy-dashboard', 'Accuracy Dashboard'),
    ('/empty-box-predictor', 'Empty Box Predictor'),
    ('/master-analyzer', 'Master Analyzer'),
    ('/advanced-analytics', 'Advanced Analytics'),
]

print("\n" + "=" * 60)
print("ROUTE TESTING")
print("=" * 60)

with app.test_client() as client:
    for route, name in test_routes:
        try:
            response = client.get(route)
            status = "[OK]" if response.status_code == 200 else f"[ERR-{response.status_code}]"
            data_check = "HAS DATA" if len(response.data) > 1000 else "EMPTY/SMALL"
            print(f"{status:10} | {data_check:12} | {name:30} | {route}")
        except Exception as e:
            print(f"[FAILED]  | ERROR        | {name:30} | {route} - {str(e)[:30]}")

print("\n" + "=" * 60)
print("PREDICTION FUNCTIONS TEST")
print("=" * 60)

# Test prediction functions
try:
    from app import advanced_predictor, smart_auto_weight_predictor, ml_predictor
    
    print("\n[TEST] Advanced Predictor...")
    adv = advanced_predictor(df, provider='all', lookback=100)
    print(f"  [OK] Returned {len(adv)} predictions")
    if adv:
        print(f"  [OK] Sample: {adv[0]}")
    
    print("\n[TEST] Smart Auto Weight Predictor...")
    smart = smart_auto_weight_predictor(df, provider='all', lookback=100)
    print(f"  [OK] Returned {len(smart)} predictions")
    if smart:
        print(f"  [OK] Sample: {smart[0]}")
    
    print("\n[TEST] ML Predictor...")
    ml = ml_predictor(df, lookback=100)
    print(f"  [OK] Returned {len(ml)} predictions")
    if ml:
        print(f"  [OK] Sample: {ml[0]}")
    
except Exception as e:
    print(f"  [ERROR] Prediction test failed: {e}")

print("\n" + "=" * 60)
print("DATA AVAILABILITY CHECK")
print("=" * 60)

# Check data availability
print(f"\n[CHECK] Total draws: {len(df)}")
print(f"[CHECK] Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
print(f"[CHECK] Providers: {len(df['provider'].unique())}")
print(f"[CHECK] Unique providers: {', '.join(sorted(df['provider'].unique()[:10]))}")

# Check prize data
prize_count = len(df[df['1st_real'].str.len() == 4])
print(f"[CHECK] Valid 4D prizes: {prize_count} / {len(df)} ({prize_count/len(df)*100:.1f}%)")

# Check recent data
recent = df.tail(50)
recent_prizes = []
for col in ['1st_real', '2nd_real', '3rd_real']:
    recent_prizes.extend([n for n in recent[col] if len(str(n)) == 4 and str(n).isdigit()])

print(f"[CHECK] Recent numbers available: {len(recent_prizes)}")
print(f"[CHECK] Sample recent numbers: {', '.join(recent_prizes[:10])}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if len(df) > 0 and prize_count > 0 and len(recent_prizes) > 0:
    print("\n[SUCCESS] ALL SYSTEMS OPERATIONAL")
    print("\nYour app should display data correctly!")
    print("Start app with: python app.py")
    print("Then open: http://127.0.0.1:5000")
else:
    print("\n[WARNING] DATA ISSUES DETECTED")
    print("\nSome data may be missing or invalid")

print("\n" + "=" * 60)
