"""
AI Pattern Predictor
Uses pattern recognition, grid analysis, and reverse logic
"""
import pandas as pd
import numpy as np
from collections import Counter
import random

def predict_ai_pattern(df, top_n=5):
    """
    Predict using AI pattern recognition
    
    Uses:
    - 4x4 grid pattern analysis
    - Reverse number patterns
    - Sequential patterns
    - Mirror patterns
    
    Returns:
        List of top N predicted numbers with scores
    """
    if len(df) == 0:
        return generate_fallback_predictions(top_n)
    
    try:
        # Analyze patterns
        patterns = analyze_patterns(df)
        
        # Generate candidates
        candidates = []
        
        # Method 1: Grid-based patterns
        grid_candidates = generate_grid_patterns(patterns, n=30)
        candidates.extend(grid_candidates)
        
        # Method 2: Reverse patterns
        reverse_candidates = generate_reverse_patterns(df, n=20)
        candidates.extend(reverse_candidates)
        
        # Method 3: Sequential patterns
        sequential_candidates = generate_sequential_patterns(patterns, n=20)
        candidates.extend(sequential_candidates)
        
        # Method 4: Mirror patterns
        mirror_candidates = generate_mirror_patterns(df, n=20)
        candidates.extend(mirror_candidates)
        
        # Score all candidates
        scored = []
        for num in candidates:
            if len(num) == 4 and num.isdigit():
                score = calculate_pattern_score(num, patterns, df)
                scored.append({
                    'number': num,
                    'score': score,
                    'method': 'ai_pattern'
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
        print(f"AI pattern prediction error: {e}")
        return generate_fallback_predictions(top_n)

def analyze_patterns(df):
    """Analyze various patterns in the data"""
    patterns = {}
    
    # Digit transition matrix (what digit follows what)
    patterns['transitions'] = {}
    for i in range(10):
        patterns['transitions'][str(i)] = Counter()
    
    for num in df['number']:
        num_str = str(num).zfill(4)
        for i in range(len(num_str) - 1):
            current = num_str[i]
            next_digit = num_str[i + 1]
            patterns['transitions'][current][next_digit] += 1
    
    # Repeating digit patterns
    patterns['repeating'] = Counter()
    for num in df['number']:
        num_str = str(num).zfill(4)
        unique_count = len(set(num_str))
        patterns['repeating'][unique_count] += 1
    
    # Ascending/descending patterns
    patterns['sequence_type'] = Counter()
    for num in df['number']:
        num_str = str(num).zfill(4)
        digits = [int(d) for d in num_str]
        if digits == sorted(digits):
            patterns['sequence_type']['ascending'] += 1
        elif digits == sorted(digits, reverse=True):
            patterns['sequence_type']['descending'] += 1
        else:
            patterns['sequence_type']['mixed'] += 1
    
    return patterns

def generate_grid_patterns(patterns, n=30):
    """Generate numbers based on grid patterns"""
    candidates = []
    
    # Use transition matrix to build numbers
    for _ in range(n):
        num_str = str(random.randint(0, 9))
        
        for _ in range(3):
            current = num_str[-1]
            if current in patterns['transitions'] and patterns['transitions'][current]:
                # Pick next digit based on transition frequency
                next_digit = random.choices(
                    list(patterns['transitions'][current].keys()),
                    weights=list(patterns['transitions'][current].values())
                )[0]
                num_str += next_digit
            else:
                num_str += str(random.randint(0, 9))
        
        candidates.append(num_str)
    
    return candidates

def generate_reverse_patterns(df, n=20):
    """Generate reverse patterns of recent numbers"""
    candidates = []
    
    recent_numbers = df['number'].tail(50).tolist()
    
    for num in random.sample(recent_numbers, min(n, len(recent_numbers))):
        num_str = str(num).zfill(4)
        reversed_num = num_str[::-1]
        candidates.append(reversed_num)
    
    return candidates

def generate_sequential_patterns(patterns, n=20):
    """Generate sequential patterns"""
    candidates = []
    
    for _ in range(n):
        start = random.randint(0, 6)
        
        # Ascending
        if random.random() > 0.5:
            num_str = ''.join([str((start + i) % 10) for i in range(4)])
        else:
            # Descending
            num_str = ''.join([str((start - i) % 10) for i in range(4)])
        
        candidates.append(num_str)
    
    return candidates

def generate_mirror_patterns(df, n=20):
    """Generate mirror patterns (ABBA, ABAB, etc.)"""
    candidates = []
    
    for _ in range(n):
        a = str(random.randint(0, 9))
        b = str(random.randint(0, 9))
        
        # Different mirror patterns
        patterns_list = [
            a + b + b + a,  # ABBA
            a + b + a + b,  # ABAB
            a + a + b + b,  # AABB
        ]
        
        candidates.append(random.choice(patterns_list))
    
    return candidates

def calculate_pattern_score(number, patterns, df):
    """Calculate pattern-based score"""
    score = 0.0
    num_str = str(number).zfill(4)
    
    # Transition score
    for i in range(len(num_str) - 1):
        current = num_str[i]
        next_digit = num_str[i + 1]
        if current in patterns['transitions']:
            score += patterns['transitions'][current].get(next_digit, 0) * 2.0
    
    # Repeating digit score
    unique_count = len(set(num_str))
    score += patterns['repeating'].get(unique_count, 0) * 1.0
    
    # Sequence type score
    digits = [int(d) for d in num_str]
    if digits == sorted(digits):
        score += patterns['sequence_type'].get('ascending', 0) * 0.5
    elif digits == sorted(digits, reverse=True):
        score += patterns['sequence_type'].get('descending', 0) * 0.5
    else:
        score += patterns['sequence_type'].get('mixed', 0) * 0.5
    
    # Recency bonus (if similar pattern appeared recently)
    recent_numbers = df['number'].tail(20).tolist()
    for recent in recent_numbers:
        similarity = calculate_similarity(num_str, str(recent).zfill(4))
        score += similarity * 10
    
    return score

def calculate_similarity(num1, num2):
    """Calculate similarity between two numbers"""
    matches = sum(1 for a, b in zip(num1, num2) if a == b)
    return matches / 4.0

def generate_fallback_predictions(top_n=5):
    """Generate fallback predictions"""
    predictions = []
    for i in range(top_n):
        num = f"{random.randint(0, 9999):04d}"
        predictions.append({
            'number': num,
            'score': 1.0,
            'method': 'ai_fallback'
        })
    return predictions


def predict_top_5(draws, mode="combined"):
    """
    Predict top 5 numbers using AI pattern analysis
    
    Args:
        draws: List of draw dictionaries with 'grid' and 'date' keys
        mode: Prediction mode (pattern, history, combined, classifier)
    
    Returns:
        Dictionary with prediction results
    """
    if not draws:
        return {"combined": []}
    
    try:
        # Convert draws to DataFrame format
        df_data = []
        for draw in draws:
            if 'grid' in draw:
                # Extract number from grid
                grid = draw['grid']
                number = ''.join([str(grid[i][i]) for i in range(min(4, len(grid)))])
                df_data.append({'number': number})
        
        if not df_data:
            return {"combined": []}
        
        df = pd.DataFrame(df_data)
        
        # Use AI pattern prediction
        predictions = predict_ai_pattern(df, top_n=5)
        
        # Format results
        result = []
        for pred in predictions:
            result.append((
                pred['number'],
                pred['score'],
                pred['method']
            ))
        
        return {"combined": result}
    
    except Exception as e:
        print(f"predict_top_5 error: {e}")
        return {"combined": []}
