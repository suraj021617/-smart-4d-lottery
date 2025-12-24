"""
XGBoost-Inspired Ensemble Predictor
Combines multiple weak predictors into strong predictor
"""
import numpy as np
from collections import Counter

def xgboost_predictor(df, lookback=150):
    """
    XGBoost-inspired ensemble (lightweight version)
    Combines frequency, patterns, and trends
    """
    try:
        # Extract numbers
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            if col in df.columns:
                all_numbers.extend([n for n in df[col].dropna() if n and len(str(n)) == 4])
        
        if len(all_numbers) < 20:
            return []
        
        recent = all_numbers[-lookback:]
        
        # Weak Learner 1: Frequency
        freq = Counter(recent)
        freq_scores = {num: count / len(recent) for num, count in freq.items()}
        
        # Weak Learner 2: Digit patterns
        digit_scores = {}
        for num in set(recent):
            digits = [int(d) for d in num]
            # Score based on digit diversity
            diversity = len(set(digits)) / 4
            digit_scores[num] = diversity
        
        # Weak Learner 3: Position patterns
        position_scores = {}
        for pos in range(4):
            pos_digits = [num[pos] for num in recent if len(num) == 4]
            pos_freq = Counter(pos_digits)
            for num in set(recent):
                if len(num) == 4:
                    score = pos_freq.get(num[pos], 0) / len(pos_digits)
                    position_scores[num] = position_scores.get(num, 0) + score
        
        # Weak Learner 4: Trend detection
        trend_scores = {}
        recent_10 = set(recent[-10:])
        recent_30 = set(recent[-30:])
        for num in set(recent):
            trend = 0
            if num in recent_10:
                trend += 2
            if num in recent_30:
                trend += 1
            trend_scores[num] = trend / 3
        
        # Ensemble: Weighted combination
        ensemble_scores = {}
        all_nums = set(freq_scores.keys()) | set(digit_scores.keys()) | set(position_scores.keys()) | set(trend_scores.keys())
        
        for num in all_nums:
            score = (
                freq_scores.get(num, 0) * 0.4 +
                digit_scores.get(num, 0) * 0.2 +
                position_scores.get(num, 0) * 0.2 +
                trend_scores.get(num, 0) * 0.2
            )
            ensemble_scores[num] = score
        
        # Sort and return top 5
        sorted_scores = sorted(ensemble_scores.items(), key=lambda x: x[1], reverse=True)
        return [(num, score, 'XGBoost-ensemble') for num, score in sorted_scores[:5]]
    
    except Exception as e:
        return []
