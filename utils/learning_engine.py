import pandas as pd
from collections import Counter
import re

def analyze_predictions_vs_results(df):
    """Analyze prediction accuracy for learning"""
    learning_data = []
    
    for i in range(len(df) - 1):
        try:
            curr_row = df.iloc[i]
            next_row = df.iloc[i + 1]
            
            # Extract predicted numbers (from current draw)
            predicted = []
            for col in ['1st_real', '2nd_real', '3rd_real']:
                num = str(curr_row.get(col, ''))
                if len(num) == 4 and num.isdigit():
                    predicted.append(num)
            
            # Extract actual numbers (from next draw)
            actual = []
            for col in ['1st_real', '2nd_real', '3rd_real']:
                num = str(next_row.get(col, ''))
                if len(num) == 4 and num.isdigit():
                    actual.append(num)
            
            if not predicted or not actual:
                continue
            
            # Calculate matches
            matches = [p for p in predicted if p in actual]
            exact = len([p for p in predicted if p in actual])
            
            # Calculate different match types
            ibox = sum(1 for p in predicted for a in actual if sorted(p) == sorted(a) and p != a)
            front = sum(1 for p in predicted for a in actual if p[:2] == a[:2])
            back = sum(1 for p in predicted for a in actual if p[2:] == a[2:])
            
            # Calculate digit matches
            digit_2 = sum(1 for p in predicted for a in actual if len(set(p) & set(a)) == 2)
            digit_3 = sum(1 for p in predicted for a in actual if len(set(p) & set(a)) == 3)
            
            # Calculate score
            score = min(100, (exact * 50) + (ibox * 30) + (front * 20) + (back * 20))
            
            learning_data.append({
                'date_from': curr_row.get('date_parsed', pd.Timestamp.now()).strftime('%d/%m/%Y'),
                'date_to': next_row.get('date_parsed', pd.Timestamp.now()).strftime('%d/%m/%Y'),
                'provider': curr_row.get('provider', 'unknown'),
                'predicted': predicted[:3],
                'actual': actual[:3],
                'has_match': len(matches) > 0,
                'matches': matches,
                'exact': exact,
                'ibox': ibox,
                'front': front,
                'back': back,
                'digit_2': digit_2,
                'digit_3': digit_3,
                'score': score
            })
            
        except Exception as e:
            continue
    
    return learning_data[:20]  # Return last 20 for display

def calculate_learning_stats(learning_data):
    """Calculate overall learning statistics"""
    if not learning_data:
        return {'total_learned': 0, 'match_rate': 0, 'confidence': 0}
    
    total_matches = sum(1 for item in learning_data if item['has_match'])
    match_rate = round((total_matches / len(learning_data)) * 100, 1)
    avg_score = round(sum(item['score'] for item in learning_data) / len(learning_data), 1)
    
    return {
        'total_learned': len(learning_data),
        'match_rate': match_rate,
        'confidence': min(95, avg_score)
    }