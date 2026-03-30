"""
Advanced Statistical Predictor
Uses frequency analysis, hot digits, pairs, triples, and transition logic
"""
import pandas as pd
from collections import Counter
import random

def predict_recent_stats(df, top_n=5):
    """
    Predict using recent statistical patterns
    
    Uses:
    - Hot digit frequency
    - Pair frequency
    - Triple patterns
    - Transition logic
    
    Returns:
        List of top N predicted numbers with scores
    """
    if len(df) == 0:
        return generate_fallback_predictions(top_n)
    
    # Analyze digit frequencies
    digit_freq = analyze_digit_frequency(df)
    
    # Analyze pair frequencies
    pair_freq = analyze_pair_frequency(df)
    
    # Analyze triple frequencies
    triple_freq = analyze_triple_frequency(df)
    
    # Generate candidate numbers
    candidates = []
    
    # Method 1: Hot digit combinations
    hot_digits = get_hot_digits(digit_freq, top=10)
    for _ in range(20):
        num = ''.join(random.choices(hot_digits, k=4))
        candidates.append(num)
    
    # Method 2: Hot pair combinations
    hot_pairs = get_hot_pairs(pair_freq, top=10)
    for pair1, pair2 in zip(hot_pairs[:10], hot_pairs[1:11]):
        num = pair1 + pair2
        candidates.append(num)
    
    # Method 3: Hot triple + hot digit
    hot_triples = get_hot_triples(triple_freq, top=10)
    for triple in hot_triples:
        for digit in hot_digits[:5]:
            candidates.append(triple + digit)
            candidates.append(digit + triple)
    
    # Score all candidates
    scored = []
    for num in candidates:
        if len(num) == 4 and num.isdigit():
            score = calculate_statistical_score(num, digit_freq, pair_freq, triple_freq)
            scored.append({'number': num, 'score': score, 'method': 'recent_stats'})
    
    # Remove duplicates and sort
    seen = set()
    unique_scored = []
    for item in scored:
        if item['number'] not in seen:
            seen.add(item['number'])
            unique_scored.append(item)
    
    unique_scored.sort(key=lambda x: x['score'], reverse=True)
    
    return unique_scored[:top_n]

def analyze_digit_frequency(df):
    """Analyze individual digit frequency (0-9)"""
    all_digits = []
    for num in df['number']:
        all_digits.extend(list(str(num)))
    
    return Counter(all_digits)

def analyze_pair_frequency(df):
    """Analyze 2-digit pair frequency"""
    all_pairs = []
    for num in df['number']:
        num_str = str(num)
        for i in range(len(num_str) - 1):
            all_pairs.append(num_str[i:i+2])
    
    return Counter(all_pairs)

def analyze_triple_frequency(df):
    """Analyze 3-digit triple frequency"""
    all_triples = []
    for num in df['number']:
        num_str = str(num)
        for i in range(len(num_str) - 2):
            all_triples.append(num_str[i:i+3])
    
    return Counter(all_triples)

def get_hot_digits(digit_freq, top=10):
    """Get most frequent digits"""
    most_common = digit_freq.most_common(top)
    return [digit for digit, _ in most_common]

def get_hot_pairs(pair_freq, top=10):
    """Get most frequent pairs"""
    most_common = pair_freq.most_common(top)
    return [pair for pair, _ in most_common]

def get_hot_triples(triple_freq, top=10):
    """Get most frequent triples"""
    most_common = triple_freq.most_common(top)
    return [triple for triple, _ in most_common]

def calculate_statistical_score(number, digit_freq, pair_freq, triple_freq):
    """Calculate statistical score for a number"""
    score = 0.0
    num_str = str(number)
    
    # Digit frequency score
    for digit in num_str:
        score += digit_freq.get(digit, 0) * 0.25
    
    # Pair frequency score
    for i in range(len(num_str) - 1):
        pair = num_str[i:i+2]
        score += pair_freq.get(pair, 0) * 0.5
    
    # Triple frequency score
    for i in range(len(num_str) - 2):
        triple = num_str[i:i+3]
        score += triple_freq.get(triple, 0) * 1.0
    
    return score

def generate_fallback_predictions(top_n=5):
    """Generate fallback predictions when no data available"""
    predictions = []
    for i in range(top_n):
        num = f"{random.randint(0, 9999):04d}"
        predictions.append({
            'number': num,
            'score': 1.0,
            'method': 'fallback'
        })
    return predictions
