"""
Smart Prediction Scorer - Auto-calculate accuracy with partial matches
"""

def calculate_digit_match(predicted, actual):
    """Count matching digits between two 4D numbers"""
    if not predicted or not actual:
        return 0
    pred_digits = set(str(predicted))
    actual_digits = set(str(actual))
    return len(pred_digits & actual_digits)

def score_prediction(predicted, actual_1st, actual_2nd, actual_3rd, special_list, consolation_list):
    """
    Score a single prediction against actual results
    Returns: (score, match_type, details)
    """
    predicted = str(predicted)
    actual_1st = str(actual_1st)
    actual_2nd = str(actual_2nd)
    actual_3rd = str(actual_3rd)
    
    # Exact matches
    if predicted == actual_1st:
        return (100, 'EXACT_1ST', f'Exact 1st Prize: {predicted}')
    if predicted == actual_2nd:
        return (80, 'EXACT_2ND', f'Exact 2nd Prize: {predicted}')
    if predicted == actual_3rd:
        return (60, 'EXACT_3RD', f'Exact 3rd Prize: {predicted}')
    
    # Special/Consolation exact
    if predicted in special_list:
        return (30, 'SPECIAL', f'Special Prize: {predicted}')
    if predicted in consolation_list:
        return (15, 'CONSOLATION', f'Consolation: {predicted}')
    
    # Partial matches (3-digit, 2-digit)
    match_1st = calculate_digit_match(predicted, actual_1st)
    match_2nd = calculate_digit_match(predicted, actual_2nd)
    match_3rd = calculate_digit_match(predicted, actual_3rd)
    
    best_match = max(match_1st, match_2nd, match_3rd)
    
    if best_match == 3:
        target = actual_1st if match_1st == 3 else (actual_2nd if match_2nd == 3 else actual_3rd)
        return (40, '3_DIGIT', f'3-digit match with {target}')
    elif best_match == 2:
        target = actual_1st if match_1st == 2 else (actual_2nd if match_2nd == 2 else actual_3rd)
        return (20, '2_DIGIT', f'2-digit match with {target}')
    
    return (0, 'MISS', 'No match')

def score_predictions(predictions, actual_results):
    """
    Score all predictions against actual results
    
    predictions: list of predicted numbers
    actual_results: dict with keys: 1st, 2nd, 3rd, special, consolation
    
    Returns: detailed scoring breakdown
    """
    results = []
    total_score = 0
    max_score = len(predictions) * 100
    
    special_list = actual_results.get('special', [])
    consolation_list = actual_results.get('consolation', [])
    
    for pred in predictions:
        score, match_type, details = score_prediction(
            pred,
            actual_results.get('1st'),
            actual_results.get('2nd'),
            actual_results.get('3rd'),
            special_list,
            consolation_list
        )
        
        results.append({
            'predicted': pred,
            'score': score,
            'match_type': match_type,
            'details': details
        })
        total_score += score
    
    accuracy = (total_score / max_score * 100) if max_score > 0 else 0
    
    return {
        'results': results,
        'total_score': total_score,
        'max_score': max_score,
        'accuracy': round(accuracy, 1),
        'rating': get_rating(accuracy)
    }

def get_rating(accuracy):
    """Get rating based on accuracy percentage"""
    if accuracy >= 90:
        return 'PERFECT'
    elif accuracy >= 70:
        return 'EXCELLENT'
    elif accuracy >= 50:
        return 'GOOD'
    elif accuracy >= 30:
        return 'FAIR'
    else:
        return 'NEEDS_IMPROVEMENT'

# Example usage
if __name__ == '__main__':
    # Example: Singapore 4D 2026-01-24
    my_predictions = ['7295', '8557', '0991', '0497', '2018']
    
    actual = {
        '1st': '7295',
        '2nd': '8557',
        '3rd': '0991',
        'special': ['0497', '0712', '2018', '2243', '2450', '4126', '4516', '4570', '5071', '9072'],
        'consolation': ['0055', '1872', '3177', '5379', '6437', '7133', '7530', '8184', '8328', '9735']
    }
    
    result = score_predictions(my_predictions, actual)
    
    print("=" * 60)
    print("PREDICTION SCORING RESULTS")
    print("=" * 60)
    
    for r in result['results']:
        print(f"\n{r['predicted']}: {r['score']} points - {r['match_type']}")
        print(f"  {r['details']}")
    
    print("\n" + "=" * 60)
    print(f"TOTAL SCORE: {result['total_score']}/{result['max_score']}")
    print(f"ACCURACY: {result['accuracy']}%")
    print(f"RATING: {result['rating']}")
    print("=" * 60)
