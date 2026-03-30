"""Number Pair & Combination Analysis"""
from collections import Counter
import pandas as pd

def analyze_pairs(df, provider=None, lookback=500, exclude_date=None):
    """Analyze digit pairs that appear together"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    # Exclude the target date from training data
    if exclude_date:
        df_filtered = df_filtered[df_filtered['date_parsed'].dt.date != exclude_date]
    
    df_filtered = df_filtered.tail(lookback)
    
    # Extract all 4D numbers
    all_numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        all_numbers.extend([n for n in nums if n.isdigit() and len(n) == 4])
    
    # Count digit pairs
    pairs = []
    for num in all_numbers:
        for i in range(len(num)-1):
            pairs.append(num[i:i+2])
    
    pair_freq = Counter(pairs).most_common(20)
    
    # Count digit triplets
    triplets = []
    for num in all_numbers:
        for i in range(len(num)-2):
            triplets.append(num[i:i+3])
    
    triplet_freq = Counter(triplets).most_common(20)
    
    # Generate predictions based on most frequent pairs
    predictions = []
    top_pairs = [pair for pair, _ in pair_freq[:5]]
    
    # Find recent numbers containing top pairs
    recent_nums = all_numbers[-100:]
    for num in set(recent_nums):
        score = sum(1 for pair in top_pairs if pair in num)
        if score > 0:
            predictions.append((num, score))
    
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'pairs': pair_freq,
        'triplets': triplet_freq,
        'total_numbers': len(all_numbers),
        'predictions': predictions[:10]
    }

def find_numbers_with_pairs(df, target_pairs, provider=None):
    """Find 4D numbers containing specific pairs"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    all_numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        all_numbers.extend([n for n in nums if n.isdigit() and len(n) == 4])
    
    # Find numbers containing target pairs
    matching = []
    for num in set(all_numbers):
        for pair in target_pairs:
            if pair in num:
                matching.append(num)
                break
    
    return list(set(matching))[:50]
