"""Quick test - verify smart-evaluate route works"""
import sys
sys.path.insert(0, '.')

try:
    from smart_scorer import score_predictions
    print("[OK] smart_scorer.py imported successfully")
    
    # Test scoring
    test_pred = ['1234', '5678']
    test_actual = {'1st': '1234', '2nd': '5678', '3rd': '9012', 'special': [], 'consolation': []}
    result = score_predictions(test_pred, test_actual)
    print(f"[OK] Scoring works: {result['total_score']}/{result['max_score']} pts")
    
    print("\n[SUCCESS] Smart scorer is ready!")
    print("Now restart your app: python app.py")
    print("Then click the button: http://localhost:5000/accuracy-dashboard")
    
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    print("\nFix: Make sure smart_scorer.py is in the same folder as app.py")
except Exception as e:
    print(f"[ERROR] {e}")
