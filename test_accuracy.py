import sys
sys.path.insert(0, 'c:\\Users\\Acer\\Desktop\\smartsuraj')

try:
    from app import app
    with app.test_request_context():
        from app import accuracy_tracker_page
        result = accuracy_tracker_page()
        print("SUCCESS: Route works!")
        print(f"Result type: {type(result)}")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
