"""
Quick verification - Check if all main routes work now
"""
from app import app

print("=" * 60)
print("QUICK ROUTE CHECK")
print("=" * 60)

routes_to_test = [
    '/',
    '/pattern-analyzer',
    '/ultimate-predictor',
    '/smart-predictor',
    '/ml-predictor',
    '/statistics',
    '/best-predictions',
]

with app.test_client() as client:
    working = 0
    broken = 0
    
    for route in routes_to_test:
        try:
            response = client.get(route)
            if response.status_code == 200:
                print(f"[OK]  {route}")
                working += 1
            else:
                print(f"[ERR] {route} - Status {response.status_code}")
                broken += 1
        except Exception as e:
            print(f"[ERR] {route} - {str(e)[:50]}")
            broken += 1

print("\n" + "=" * 60)
print(f"RESULT: {working} working, {broken} broken")
print("=" * 60)

if broken == 0:
    print("\n[SUCCESS] All main routes working!")
    print("Start app: python app.py")
    print("Open: http://127.0.0.1:5000")
else:
    print(f"\n[WARNING] {broken} routes still have issues")
