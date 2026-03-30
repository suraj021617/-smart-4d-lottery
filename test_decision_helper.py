"""
Test decision-helper route
"""
import sys
sys.path.insert(0, '.')

print("Testing decision-helper route...")

try:
    import app
    
    # Create test client
    with app.app.test_client() as client:
        print("\n[TEST] Accessing /decision-helper route...")
        response = client.get('/decision-helper')
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("[SUCCESS] Route works! Page loaded successfully.")
        elif response.status_code == 404:
            print("[ERROR] 404 Not Found - Route not registered")
        elif response.status_code == 500:
            print("[ERROR] 500 Internal Server Error")
            print(f"Error: {response.data.decode()[:500]}")
        else:
            print(f"[WARNING] Unexpected status: {response.status_code}")
            
except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()
