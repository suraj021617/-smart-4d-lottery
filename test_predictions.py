#!/usr/bin/env python
# Test Pattern Analyzer predictions

from app import load_csv_data
from utils.app_grid import generate_4x4_grid
from utils.pattern_finder import find_all_4digit_patterns
from utils.ai_predictor import predict_top_5

# Load data
df = load_csv_data()
print(f"Loaded {len(df)} rows")

# Get latest draw
if not df.empty:
    latest = df.iloc[0]  # df is sorted descending
    number = str(latest['number_1st'])
    print(f"\nLatest draw: {latest['date_parsed'].date()} - {latest['provider_key']} - {number}")
    
    # Generate grid
    grid = generate_4x4_grid(number)
    print(f"\nGrid for {number}:")
    for i, row in enumerate(grid, 1):
        print(f"Row {i}: {row}")
    
    # Find patterns
    patterns = find_all_4digit_patterns(grid)
    print(f"\nTotal patterns: {len(patterns)}")
    
    # Get unique 4D patterns
    unique = list(set([p for _, _, p, _ in patterns]))
    print(f"Unique 4D numbers in patterns: {len(unique)}")
    print(f"Sample patterns: {unique[:10]}")
    
    # Test AI predictor
    print("\n" + "="*60)
    print("TESTING AI PREDICTOR")
    print("="*60)
    
    draw_data = [{'date': str(latest['date_parsed'].date()), 'grid': grid}]
    
    for mode in ['pattern', 'combined']:
        print(f"\nMode: {mode}")
        try:
            predictions = predict_top_5(draw_data, mode=mode)
            print(f"Predictions type: {type(predictions)}")
            print(f"Predictions: {predictions}")
            
            if isinstance(predictions, dict):
                for key, vals in predictions.items():
                    print(f"  {key}: {vals[:3] if vals else 'empty'}")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
