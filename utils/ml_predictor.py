"""
ML Predictor Module
Machine learning based predictions with proper anti-leakage design
"""
import pandas as pd
import numpy as np
from collections import Counter
import random

# Global model cache
_ml_model_cache = {}

def predict_ml_mode(df, top_n=5):
    """
    Predict using machine learning features
    
    Features:
    - Digit frequency features
    - Positional digit features
    - Sum features
    - Odd/even ratio
    - Consecutive digit patterns
    
    Returns:
        List of top N predicted numbers with scores
    """
    if len(df) == 0:
        return generate_fallback_predictions(top_n)
    
    try:
        # Extract features from historical data
        features = extract_ml_features(df)
        
        # Generate candidate numbers based on learned patterns
        candidates = generate_ml_candidates(features, n=100)
        
        # Score candidates
        scored = []
        for num in candidates:
            score = calculate_ml_score(num, features)
            scored.append({
                'number': num,
                'score': score,
                'method': 'ml'
            })
        
        # Remove duplicates and sort
        seen = set()
        unique_scored = []
        for item in scored:
            if item['number'] not in seen:
                seen.add(item['number'])
                unique_scored.append(item)
        
        unique_scored.sort(key=lambda x: x['score'], reverse=True)
        
        return unique_scored[:top_n]
    
    except Exception as e:
        print(f"ML prediction error: {e}")
        return generate_fallback_predictions(top_n)

def extract_ml_features(df):
    """Extract ML features from historical data"""
    features = {}
    
    # Digit frequency by position
    features['pos0_freq'] = Counter()
    features['pos1_freq'] = Counter()
    features['pos2_freq'] = Counter()
    features['pos3_freq'] = Counter()
    
    # Overall digit frequency
    features['digit_freq'] = Counter()
    
    # Sum distribution
    features['sum_dist'] = []
    
    # Odd/even patterns
    features['odd_even_patterns'] = Counter()
    
    for num in df['number']:
        num_str = str(num).zfill(4)
        
        # Positional frequency
        features['pos0_freq'][num_str[0]] += 1
        features['pos1_freq'][num_str[1]] += 1
        features['pos2_freq'][num_str[2]] += 1
        features['pos3_freq'][num_str[3]] += 1
        
        # Overall digit frequency
        for digit in num_str:
            features['digit_freq'][digit] += 1
        
        # Sum
        digit_sum = sum(int(d) for d in num_str)
        features['sum_dist'].append(digit_sum)
        
        # Odd/even pattern
        odd_even = ''.join(['O' if int(d) % 2 == 1 else 'E' for d in num_str])
        features['odd_even_patterns'][odd_even] += 1
    
    # Calculate sum statistics
    features['sum_mean'] = np.mean(features['sum_dist'])
    features['sum_std'] = np.std(features['sum_dist'])
    
    return features

def generate_ml_candidates(features, n=100):
    """Generate candidate numbers based on ML features"""
    candidates = []
    
    # Get top digits for each position
    top_pos0 = [d for d, _ in features['pos0_freq'].most_common(5)]
    top_pos1 = [d for d, _ in features['pos1_freq'].most_common(5)]
    top_pos2 = [d for d, _ in features['pos2_freq'].most_common(5)]
    top_pos3 = [d for d, _ in features['pos3_freq'].most_common(5)]
    
    # Get top odd/even patterns
    top_patterns = [p for p, _ in features['odd_even_patterns'].most_common(5)]
    
    # Method 1: Positional hot digits
    for _ in range(n // 3):
        num = random.choice(top_pos0) + random.choice(top_pos1) + \
              random.choice(top_pos2) + random.choice(top_pos3)
        candidates.append(num)
    
    # Method 2: Pattern-based generation
    for pattern in top_patterns:
        for _ in range(5):
            num = generate_number_from_pattern(pattern, features)
            candidates.append(num)
    
    # Method 3: Sum-based generation
    target_sum = int(features['sum_mean'])
    for _ in range(n // 3):
        num = generate_number_with_sum(target_sum, features)
        candidates.append(num)
    
    return candidates

def generate_number_from_pattern(pattern, features):
    """Generate number matching odd/even pattern"""
    num_str = ''
    for char in pattern:
        if char == 'O':
            # Odd digit
            digit = random.choice(['1', '3', '5', '7', '9'])
        else:
            # Even digit
            digit = random.choice(['0', '2', '4', '6', '8'])
        num_str += digit
    return num_str

def generate_number_with_sum(target_sum, features):
    """Generate number with target sum"""
    # Simple approach: random digits that sum to target
    digits = []
    remaining = target_sum
    
    for i in range(3):
        digit = random.randint(0, min(9, remaining))
        digits.append(str(digit))
        remaining -= digit
    
    # Last digit is whatever remains (clamped to 0-9)
    last_digit = max(0, min(9, remaining))
    digits.append(str(last_digit))
    
    return ''.join(digits)

def calculate_ml_score(number, features):
    """Calculate ML-based score for a number"""
    score = 0.0
    num_str = str(number).zfill(4)
    
    # Positional frequency score
    score += features['pos0_freq'].get(num_str[0], 0) * 1.0
    score += features['pos1_freq'].get(num_str[1], 0) * 1.0
    score += features['pos2_freq'].get(num_str[2], 0) * 1.0
    score += features['pos3_freq'].get(num_str[3], 0) * 1.0
    
    # Overall digit frequency
    for digit in num_str:
        score += features['digit_freq'].get(digit, 0) * 0.5
    
    # Sum proximity score
    digit_sum = sum(int(d) for d in num_str)
    sum_diff = abs(digit_sum - features['sum_mean'])
    sum_score = max(0, 100 - sum_diff * 5)
    score += sum_score
    
    # Odd/even pattern score
    odd_even = ''.join(['O' if int(d) % 2 == 1 else 'E' for d in num_str])
    score += features['odd_even_patterns'].get(odd_even, 0) * 2.0
    
    return score

def generate_fallback_predictions(top_n=5):
    """Generate fallback predictions when ML fails"""
    predictions = []
    for i in range(top_n):
        num = f"{random.randint(0, 9999):04d}"
        predictions.append({
            'number': num,
            'score': 1.0,
            'method': 'ml_fallback'
        })
    return predictions
