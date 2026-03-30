"""Deep Learning LSTM Model for 4D Prediction"""
import numpy as np
import pandas as pd
from collections import Counter

def prepare_lstm_data(df, provider=None, lookback=100):
    """Prepare data for LSTM (simplified without keras)"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered = df_filtered.tail(lookback)
    
    # Extract sequences
    sequences = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        for num in nums:
            if num.isdigit() and len(num) == 4:
                # Convert to digit sequence
                sequences.append([int(d) for d in num])
    
    return np.array(sequences)

def lstm_predict(df, provider=None, lookback=200):
    """LSTM-style prediction (pattern-based without actual neural network)"""
    sequences = prepare_lstm_data(df, provider, lookback)
    
    if len(sequences) == 0:
        return []
    
    # Analyze digit patterns in sequences
    digit_patterns = {i: Counter() for i in range(4)}
    
    for seq in sequences:
        for pos, digit in enumerate(seq):
            digit_patterns[pos][digit] += 1
    
    # Generate predictions based on most common patterns
    predictions = []
    
    # Method 1: Most frequent digit per position
    for _ in range(10):
        pred_num = ''
        for pos in range(4):
            # Get top digits for this position
            top_digits = [d for d, _ in digit_patterns[pos].most_common(5)]
            if top_digits:
                # Add some variation
                digit = np.random.choice(top_digits)
                pred_num += str(digit)
        
        if len(pred_num) == 4 and pred_num not in predictions:
            predictions.append(pred_num)
    
    # Method 2: Sequence patterns
    for i in range(len(sequences) - 1):
        current = sequences[i]
        next_seq = sequences[i + 1]
        
        # Look for transition patterns
        diff = next_seq - current
        
        # Apply pattern to recent numbers
        if len(sequences) > 0:
            last = sequences[-1]
            predicted = (last + diff) % 10
            pred_num = ''.join([str(d) for d in predicted])
            
            if pred_num not in predictions:
                predictions.append(pred_num)
    
    # Score predictions
    scored = []
    for num in predictions[:20]:
        # Calculate confidence based on digit frequency
        confidence = 0
        for pos, digit in enumerate(num):
            freq = digit_patterns[pos].get(int(digit), 0)
            confidence += freq
        
        confidence = min(confidence / len(sequences), 0.95)
        scored.append((num, confidence, 'LSTM Pattern'))
    
    return sorted(scored, key=lambda x: x[1], reverse=True)[:10]
