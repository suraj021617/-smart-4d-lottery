"""
LSTM Neural Network Predictor for 4D Lottery
Learns sequences from historical draws
"""
import numpy as np
import pandas as pd
from collections import Counter

def lstm_predictor(df, lookback=100):
    """
    LSTM-inspired predictor (lightweight version without TensorFlow)
    Uses sequence patterns and weighted history
    """
    try:
        # Extract numbers
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            if col in df.columns:
                all_numbers.extend([n for n in df[col].dropna() if n and len(str(n)) == 4])
        
        if len(all_numbers) < 20:
            return []
        
        # Use recent history
        recent = all_numbers[-lookback:]
        
        # Sequence learning: what follows what
        sequences = {}
        for i in range(len(recent) - 1):
            curr = recent[i]
            next_num = recent[i + 1]
            if curr not in sequences:
                sequences[curr] = []
            sequences[curr].append(next_num)
        
        # Score candidates based on sequence strength
        candidates = {}
        for num, followers in sequences.items():
            for follower in followers:
                weight = followers.count(follower) / len(followers)
                candidates[follower] = candidates.get(follower, 0) + weight
        
        # Add recency bias (recent numbers weighted more)
        for i, num in enumerate(recent[-20:]):
            recency_weight = (i + 1) / 20
            candidates[num] = candidates.get(num, 0) + recency_weight
        
        # Sort and return top 5
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return [(num, score, 'LSTM-sequence') for num, score in sorted_candidates[:5]]
    
    except Exception as e:
        return []
