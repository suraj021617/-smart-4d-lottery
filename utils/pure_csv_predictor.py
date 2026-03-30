"""
PURE CSV PREDICTOR - NO FAKE, NO RANDOM
Only uses REAL data from CSV file
"""
from collections import Counter
import pandas as pd

def pure_csv_predictor(df, lookback=200):
    """
    100% REAL predictions from CSV data only
    NO random generation, NO fake candidates
    """
    if df.empty:
        return []
    
    # Extract ONLY 4D numbers from CSV
    all_numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        if col in df.columns:
            for val in df[col].dropna():
                num_str = str(val).strip()
                if len(num_str) == 4 and num_str.isdigit():
                    all_numbers.append(num_str)
    
    if not all_numbers:
        return []
    
    # Use ONLY recent numbers from CSV (df sorted descending)
    recent = all_numbers[:lookback]
    
    # Count digit frequency from ACTUAL CSV data
    digit_freq = Counter(''.join(recent))
    
    # Count digit pairs from ACTUAL CSV data
    pair_freq = Counter()
    for num in recent:
        for i in range(3):
            pair_freq[num[i:i+2]] += 1
    
    # Score ONLY numbers that ACTUALLY appeared in CSV
    scored = {}
    for num in set(recent):
        score = 0
        reasons = []
        
        # 1. Hot digit score (how often digits appear in CSV)
        digit_score = sum(digit_freq.get(d, 0) for d in num)
        score += digit_score
        reasons.append(f"digits:{digit_score}")
        
        # 2. Pair frequency (how often digit pairs appear in CSV)
        pair_score = sum(pair_freq.get(num[i:i+2], 0) for i in range(3))
        score += pair_score * 0.5
        reasons.append(f"pairs:{pair_score}")
        
        # 3. Recency (appeared recently in CSV)
        if num in recent[:20]:
            score += 5
            reasons.append("recent")
        
        scored[num] = (score, '+'.join(reasons))
    
    # Sort by score
    sorted_nums = sorted(scored.items(), key=lambda x: x[1][0], reverse=True)
    
    # Normalize scores to 0-1
    if sorted_nums:
        max_score = sorted_nums[0][1][0]
        result = [(num, score/max_score if max_score > 0 else 0, reason) 
                  for num, (score, reason) in sorted_nums[:10]]
        return result[:5]
    
    return []
