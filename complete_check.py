"""
COMPLETE TEMPLATE & DATA CHECK
Tests if pages actually show data to users
"""
from app import app, load_csv_data

print("=" * 70)
print("COMPLETE TEMPLATE & PREDICTION DATA CHECK")
print("=" * 70)

# Load data
df = load_csv_data()
print(f"\n[DATA] Loaded: {len(df)} rows")

# Test each route and check response content
test_routes = [
    ('/', 'Home Dashboard', ['Latest Results', 'cards', 'provider']),
    ('/ultimate-predictor', 'Ultimate Predictor', ['Ultimate', 'predictions', 'consensus']),
    ('/smart-predictor', 'Smart Predictor', ['Smart', 'predictions', 'auto-w']),
    ('/ml-predictor', 'ML Predictor', ['ML', 'predictions', 'learned']),
    ('/statistics', 'Statistics', ['Statistics', 'Total', 'frequency']),
    ('/best-predictions', 'Best Predictions', ['Best', 'predictions', 'confidence']),
    ('/pattern-analyzer', 'Pattern Analyzer', ['Pattern', 'grid', 'analysis']),
    ('/frequency-analyzer', 'Frequency Analyzer', ['Frequency', 'hot', 'cold']),
    ('/hot-cold', 'Hot/Cold', ['Hot', 'Cold', 'Numbers']),
    ('/quick-pick', 'Quick Pick', ['Quick', 'Pick', 'numbers']),
]

print("\n" + "=" * 70)
print("CHECKING EACH PAGE...")
print("=" * 70)

with app.test_client() as client:
    for route, name, keywords in test_routes:
        try:
            response = client.get(route)
            status = response.status_code
            content = response.data.decode('utf-8', errors='ignore')
            
            # Check status
            status_ok = status == 200
            
            # Check if has substantial content
            has_content = len(content) > 5000
            
            # Check if keywords present
            keyword_found = sum(1 for kw in keywords if kw.lower() in content.lower())
            
            # Check if has actual numbers (predictions/data)
            has_numbers = content.count('class="') > 10  # Has HTML elements
            
            # Overall assessment
            if status_ok and has_content and keyword_found >= 2:
                result = "[OK]"
                detail = f"Content: {len(content)} bytes, Keywords: {keyword_found}/{len(keywords)}"
            elif status_ok and has_content:
                result = "[PARTIAL]"
                detail = f"Loads but may be missing data. Keywords: {keyword_found}/{len(keywords)}"
            elif status_ok:
                result = "[EMPTY]"
                detail = f"Page loads but very little content ({len(content)} bytes)"
            else:
                result = "[ERROR]"
                detail = f"HTTP {status}"
            
            print(f"\n{result:12} {name:25}")
            print(f"             {detail}")
            
            # Show sample of what's actually displayed
            if status_ok and has_content:
                # Extract some visible text (not HTML tags)
                import re
                text_only = re.sub(r'<[^>]+>', ' ', content)
                text_only = ' '.join(text_only.split())[:200]
                if text_only:
                    print(f"             Preview: {text_only[:150]}...")
            
        except Exception as e:
            print(f"\n[FAILED]     {name:25}")
            print(f"             Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("PREDICTION FUNCTION TEST")
print("=" * 70)

try:
    from app import advanced_predictor, smart_auto_weight_predictor, ml_predictor
    
    print("\n[TEST] Advanced Predictor...")
    adv = advanced_predictor(df, provider='all', lookback=50)
    if adv and len(adv) > 0:
        print(f"  [OK] Returns {len(adv)} predictions")
        print(f"  [OK] Sample: {adv[0]}")
        print(f"  [OK] All predictions: {[p[0] for p in adv]}")
    else:
        print(f"  [EMPTY] No predictions returned!")
    
    print("\n[TEST] Smart Predictor...")
    smart = smart_auto_weight_predictor(df, provider='all', lookback=50)
    if smart and len(smart) > 0:
        print(f"  [OK] Returns {len(smart)} predictions")
        print(f"  [OK] Sample: {smart[0]}")
        print(f"  [OK] All predictions: {[p[0] for p in smart]}")
    else:
        print(f"  [EMPTY] No predictions returned!")
    
    print("\n[TEST] ML Predictor...")
    ml = ml_predictor(df, lookback=50)
    if ml and len(ml) > 0:
        print(f"  [OK] Returns {len(ml)} predictions")
        print(f"  [OK] Sample: {ml[0]}")
        print(f"  [OK] All predictions: {[p[0] for p in ml]}")
    else:
        print(f"  [EMPTY] No predictions returned!")
    
except Exception as e:
    print(f"  [ERROR] {e}")

print("\n" + "=" * 70)
print("FINAL VERDICT")
print("=" * 70)

print("\nIf you see [OK] or [PARTIAL] above, those pages are showing data.")
print("If you see [EMPTY] or [ERROR], those pages have issues.")
print("\nStart app with: python app.py")
print("Then check: http://127.0.0.1:5000")
print("\n" + "=" * 70)
