"""
Enhanced Day-to-Day Pattern Predictor with Advanced Logic
"""
from collections import Counter, defaultdict
import numpy as np
from datetime import datetime, timedelta

def enhanced_day_to_day_predictor(df, today_numbers):
    """
    Advanced day-to-day prediction with multiple algorithms
    """
    predictions = []
    
    # Algorithm 1: Transition Matrix Analysis
    transition_preds = transition_matrix_prediction(df, today_numbers)
    predictions.extend([(num, score, "Transition Matrix") for num, score in transition_preds])
    
    # Algorithm 2: Momentum Analysis
    momentum_preds = momentum_based_prediction(df, today_numbers)
    predictions.extend([(num, score, "Momentum Analysis") for num, score in momentum_preds])
    
    # Algorithm 3: Pattern Completion
    pattern_preds = pattern_completion_prediction(df, today_numbers)
    predictions.extend([(num, score, "Pattern Completion") for num, score in pattern_preds])
    
    # Algorithm 4: Cyclical Analysis
    cyclical_preds = cyclical_prediction(df, today_numbers)
    predictions.extend([(num, score, "Cyclical Pattern") for num, score in cyclical_preds])
    
    # Combine and rank predictions
    combined = combine_predictions(predictions)
    return combined[:10]

def transition_matrix_prediction(df, today_numbers):
    """Build transition matrix from historical data"""
    if not today_numbers:
        return []
    
    # Build transition matrix
    transitions = defaultdict(lambda: defaultdict(int))
    
    all_numbers = []
    for col in ['1st_real', '2nd_real', '3rd_real']:
        all_numbers.extend([n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    # Learn transitions
    for i in range(len(all_numbers) - 1):
        current = all_numbers[i]
        next_num = all_numbers[i + 1]
        transitions[current][next_num] += 1
    
    # Predict based on today's numbers
    predictions = []
    for today_num in today_numbers:
        if today_num in transitions:
            total = sum(transitions[today_num].values())
            for next_num, count in transitions[today_num].items():
                probability = count / total
                predictions.append((next_num, probability))
    
    return sorted(predictions, key=lambda x: x[1], reverse=True)[:5]

def momentum_based_prediction(df, today_numbers):
    """Predict based on number momentum"""
    if len(df) < 20:
        return []
    
    # Calculate momentum for each number
    recent_10 = df.tail(10)
    previous_10 = df.tail(20).head(10)
    
    recent_nums = []
    previous_nums = []
    
    for col in ['1st_real', '2nd_real', '3rd_real']:
        recent_nums.extend([n for n in recent_10[col].astype(str) if len(n) == 4 and n.isdigit()])
        previous_nums.extend([n for n in previous_10[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    recent_freq = Counter(recent_nums)
    previous_freq = Counter(previous_nums)
    
    momentum_scores = {}
    for num in set(recent_nums + previous_nums):
        recent_count = recent_freq.get(num, 0)
        previous_count = previous_freq.get(num, 0)
        
        # Calculate momentum
        if previous_count > 0:
            momentum = recent_count / previous_count
        else:
            momentum = recent_count * 2  # New numbers get boost
        
        momentum_scores[num] = momentum
    
    # Sort by momentum
    sorted_momentum = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_momentum[:5]

def pattern_completion_prediction(df, today_numbers):
    """Predict numbers that complete patterns"""
    if not today_numbers:
        return []
    
    predictions = []
    
    for today_num in today_numbers:
        digits = [int(d) for d in today_num]
        
        # Pattern 1: Arithmetic progression completion
        for step in range(1, 4):
            # Forward progression
            next_digits = [(d + step) % 10 for d in digits]
            next_num = ''.join(map(str, next_digits))
            predictions.append((next_num, 0.3))
            
            # Backward progression
            prev_digits = [(d - step) % 10 for d in digits]
            prev_num = ''.join(map(str, prev_digits))
            predictions.append((prev_num, 0.25))
        
        # Pattern 2: Mirror/Reverse patterns
        reversed_num = today_num[::-1]
        predictions.append((reversed_num, 0.4))
        
        # Pattern 3: Digit rotation
        for i in range(1, 4):
            rotated = today_num[i:] + today_num[:i]
            predictions.append((rotated, 0.2))
    
    return predictions

def cyclical_prediction(df, today_numbers):
    """Predict based on 3-4 day lottery cycle patterns"""
    if len(df) < 30:
        return []
    
    # Malaysian 4D schedule: Tue/Wed/Sat/Sun (3-4 days per week)
    df['day_of_week'] = df['date_parsed'].dt.dayofweek
    
    # Focus on actual draw days only
    draw_days = [1, 2, 5, 6]  # Tue, Wed, Sat, Sun
    draw_day_df = df[df['day_of_week'].isin(draw_days)]
    
    # Get next expected draw day
    today = datetime.now()
    next_draw_day = None
    for i in range(1, 8):
        check_date = today + timedelta(days=i)
        if check_date.weekday() in draw_days:
            next_draw_day = check_date.weekday()
            break
    
    if next_draw_day is None:
        return []
    
    # Get numbers from same weekday in history
    same_dow_df = draw_day_df[draw_day_df['day_of_week'] == next_draw_day]
    
    cyclical_nums = []
    for col in ['1st_real', '2nd_real', '3rd_real']:
        cyclical_nums.extend([n for n in same_dow_df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    if not cyclical_nums:
        return []
    
    freq = Counter(cyclical_nums)
    total = len(cyclical_nums)
    
    # Boost predictions based on 3-4 day cycle strength
    day_names = {1: 'Tuesday', 2: 'Wednesday', 5: 'Saturday', 6: 'Sunday'}
    day_name = day_names.get(next_draw_day, 'Unknown')
    
    predictions = []
    for num, count in freq.most_common(10):
        confidence = (count / total) * 1.2  # Boost for cycle accuracy
        predictions.append((num, confidence))
    
    return predictions

def combine_predictions(predictions):
    """Combine predictions from multiple algorithms"""
    combined_scores = defaultdict(float)
    method_counts = defaultdict(int)
    
    # Weight different methods
    method_weights = {
        "Transition Matrix": 1.2,
        "Momentum Analysis": 1.0,
        "Pattern Completion": 0.8,
        "Cyclical Pattern": 0.9
    }
    
    for num, score, method in predictions:
        weight = method_weights.get(method, 1.0)
        combined_scores[num] += score * weight
        method_counts[num] += 1
    
    # Boost numbers predicted by multiple methods
    for num in combined_scores:
        if method_counts[num] > 1:
            combined_scores[num] *= (1 + method_counts[num] * 0.1)
    
    # Sort and format
    sorted_predictions = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    
    result = []
    for num, score in sorted_predictions:
        confidence = min(score * 100, 95)  # Cap at 95%
        methods_used = method_counts[num]
        reason = f"Consensus from {methods_used} method(s)"
        result.append((num, confidence, reason))
    
    return result