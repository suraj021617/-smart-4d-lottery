"""
Auto-Evaluate Predictions - Compare with new results from CSV
Run this after uploading new draw results
"""
import pandas as pd
import json
from datetime import datetime
from smart_scorer import score_predictions

def load_predictions(date, provider):
    """Load saved predictions for specific date/provider"""
    try:
        with open('prediction_tracking.csv', 'r') as f:
            df = pd.read_csv('prediction_tracking.csv')
            match = df[(df['draw_date'].str.contains(date)) & (df['provider'] == provider)]
            if not match.empty:
                pred_str = match.iloc[0]['predicted_numbers']
                # Parse prediction string
                import re
                numbers = re.findall(r'\d{4}', pred_str)
                return numbers[:5]
    except:
        pass
    return None

def get_latest_results():
    """Get latest results from CSV"""
    from utils.data_normalizer import normalize_dataframe
    
    df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')
    df = normalize_dataframe(df)
    df = df[df['is_valid']].sort_values('date_parsed', ascending=False)
    
    results = []
    for _, row in df.head(20).iterrows():
        special = str(row.get('special', '')).split()
        consolation = str(row.get('consolation', '')).split()
        
        results.append({
            'date': row['date_parsed'].strftime('%Y-%m-%d'),
            'provider': row['provider_key'],
            '1st': row['number_1st'],
            '2nd': row['number_2nd'],
            '3rd': row['number_3rd'],
            'special': [n for n in special if n and n != '----'],
            'consolation': [n for n in consolation if n and n != '----']
        })
    
    return results

def auto_evaluate():
    """Auto-evaluate all pending predictions"""
    print("=" * 60)
    print("AUTO-EVALUATION - Checking predictions vs actual results")
    print("=" * 60)
    
    latest_results = get_latest_results()
    
    if not latest_results:
        print("\nNo results found in CSV")
        return
    
    print(f"\nFound {len(latest_results)} recent draws")
    
    evaluated = []
    
    for result in latest_results:
        date = result['date']
        provider = result['provider']
        
        # Check if we have predictions for this draw
        predictions = load_predictions(date, provider)
        
        if predictions:
            print(f"\n{'='*60}")
            print(f"Date: {date} | Provider: {provider}")
            print(f"{'='*60}")
            
            score_result = score_predictions(predictions, result)
            
            print(f"\nPredictions: {', '.join(predictions)}")
            print(f"Winners: {result['1st']}, {result['2nd']}, {result['3rd']}")
            
            print(f"\nDetailed Breakdown:")
            for r in score_result['results']:
                emoji = '✅' if r['score'] >= 60 else '⭐' if r['score'] >= 30 else '🎯' if r['score'] > 0 else '❌'
                print(f"  {emoji} {r['predicted']}: {r['score']} pts - {r['details']}")
            
            print(f"\n{'='*60}")
            print(f"TOTAL: {score_result['total_score']}/{score_result['max_score']} points")
            print(f"ACCURACY: {score_result['accuracy']}%")
            print(f"RATING: {score_result['rating']}")
            print(f"{'='*60}")
            
            evaluated.append({
                'date': date,
                'provider': provider,
                'accuracy': score_result['accuracy'],
                'rating': score_result['rating'],
                'total_score': score_result['total_score']
            })
    
    if evaluated:
        print(f"\n\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        avg_accuracy = sum(e['accuracy'] for e in evaluated) / len(evaluated)
        print(f"Evaluated: {len(evaluated)} predictions")
        print(f"Average Accuracy: {avg_accuracy:.1f}%")
        print(f"Best: {max(evaluated, key=lambda x: x['accuracy'])['accuracy']}%")
        print(f"{'='*60}")
    else:
        print("\nNo matching predictions found for recent draws")
        print("Make predictions first, then upload new results!")

if __name__ == '__main__':
    auto_evaluate()
