"""Test script - no emojis"""
import sys
sys.path.insert(0, '.')

try:
    from app import app
    
    print("=" * 60)
    print("OK: App loaded!")
    print("=" * 60)
    
    routes = [str(r) for r in app.url_map.iter_rules() if r.endpoint != 'static']
    advanced = [r for r in routes if any(x in r for x in ['accuracy', 'pair', 'time', 'overdue', 'box', 'lstm', 'ensemble', 'odds', 'advanced-features'])]
    
    print(f"\nADVANCED FEATURES ({len(advanced)}/8):")
    for r in sorted(advanced):
        print(f"  {r}")
    
    print(f"\nTotal routes: {len(routes)}")
    print("\nAccess at: http://127.0.0.1:5000/advanced-features")
    print("=" * 60)
    
except Exception as e:
    print(f"ERROR: {e}")
