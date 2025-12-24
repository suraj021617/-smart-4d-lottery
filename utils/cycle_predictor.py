"""
3-4 Day Lottery Cycle Predictor
Specialized for Malaysian 4D lottery schedule
"""
from collections import Counter, defaultdict
from datetime import datetime, timedelta

def predict_next_cycle_numbers(df, provider='all'):
    """
    Predict numbers based on 3-4 day lottery cycle
    Malaysian 4D: Tue/Wed/Sat/Sun (3-4 times per week)
    """
    if df.empty:
        return []
    
    # Define draw days (0=Monday, 6=Sunday)
    draw_days = [1, 2, 5, 6]  # Tue, Wed, Sat, Sun
    
    # Filter to only draw days
    df['day_of_week'] = df['date_parsed'].dt.dayofweek
    draw_df = df[df['day_of_week'].isin(draw_days)]
    
    if draw_df.empty:
        return []
    
    # Get next draw day
    today = datetime.now()
    next_draw_day = None
    days_until_draw = 0
    
    for i in range(1, 8):
        check_date = today + timedelta(days=i)
        if check_date.weekday() in draw_days:
            next_draw_day = check_date.weekday()
            days_until_draw = i
            break
    
    if next_draw_day is None:
        return []
    
    predictions = []
    
    # Method 1: Same weekday historical pattern
    same_day_predictions = analyze_same_weekday_pattern(draw_df, next_draw_day)
    predictions.extend(same_day_predictions)
    
    # Method 2: 3-4 day cycle momentum
    cycle_predictions = analyze_cycle_momentum(draw_df, days_until_draw)
    predictions.extend(cycle_predictions)
    
    # Method 3: Gap analysis (numbers overdue based on 3-4 day cycle)
    gap_predictions = analyze_cycle_gaps(draw_df, next_draw_day)
    predictions.extend(gap_predictions)
    
    # Combine and rank
    combined = combine_cycle_predictions(predictions)
    
    return combined[:10]

def analyze_same_weekday_pattern(df, target_weekday):
    """Analyze numbers that appear on the same weekday"""
    same_day_df = df[df['day_of_week'] == target_weekday]
    
    if same_day_df.empty:
        return []
    
    numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        numbers.extend([n for n in same_day_df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    if not numbers:
        return []
    
    freq = Counter(numbers)
    total = len(numbers)
    
    day_names = {1: 'Tuesday', 2: 'Wednesday', 5: 'Saturday', 6: 'Sunday'}
    day_name = day_names.get(target_weekday, 'Unknown')
    
    predictions = []
    for num, count in freq.most_common(15):
        confidence = (count / total) * 100
        reason = f"{day_name} pattern (appeared {count}/{total} times)"
        predictions.append((num, confidence, reason))
    
    return predictions

def analyze_cycle_momentum(df, days_until_draw):
    """Analyze momentum based on 3-4 day cycle"""
    if len(df) < 12:  # Need at least 3-4 cycles
        return []
    
    # Get last 3 cycles (9-12 draws)
    recent_cycles = df.tail(12)
    
    # Calculate momentum
    all_numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        all_numbers.extend([n for n in recent_cycles[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    if not all_numbers:
        return []
    
    # Numbers gaining momentum (appearing more frequently in recent cycles)
    freq = Counter(all_numbers)
    
    predictions = []
    for num, count in freq.most_common(10):
        # Boost based on days until draw (closer = higher confidence)
        momentum_score = count * (4 - days_until_draw) / 3
        confidence = min(momentum_score * 10, 85)
        reason = f"Cycle momentum (appeared {count} times in last 3 cycles)"
        predictions.append((num, confidence, reason))
    
    return predictions

def analyze_cycle_gaps(df, target_weekday):
    """Find numbers overdue based on 3-4 day cycle"""
    if len(df) < 20:
        return []
    
    # Get all numbers and their last appearance
    all_numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        all_numbers.extend([n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    if not all_numbers:
        return []
    
    # Find numbers that haven't appeared recently
    recent_numbers = set()
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        recent_numbers.update([n for n in df.tail(6)[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    # Get historical frequency
    historical_freq = Counter(all_numbers)
    
    # Find overdue numbers
    overdue_predictions = []
    for num, total_count in historical_freq.most_common(50):
        if num not in recent_numbers and total_count >= 3:
            # Calculate overdue score
            expected_frequency = total_count / len(df) * 6  # Expected in last 6 draws
            if expected_frequency > 0.5:  # Should have appeared at least once
                overdue_score = min(expected_frequency * 20, 70)
                reason = f"Overdue (expected {expected_frequency:.1f} times in last 6 draws)"
                overdue_predictions.append((num, overdue_score, reason))
    
    return sorted(overdue_predictions, key=lambda x: x[1], reverse=True)[:8]

def combine_cycle_predictions(predictions):
    """Combine predictions from different cycle analysis methods"""
    combined_scores = defaultdict(lambda: {'score': 0, 'reasons': [], 'method_count': 0})
    
    for num, score, reason in predictions:
        combined_scores[num]['score'] += score
        combined_scores[num]['reasons'].append(reason)
        combined_scores[num]['method_count'] += 1
    
    # Boost numbers predicted by multiple methods
    final_predictions = []
    for num, data in combined_scores.items():
        # Multi-method bonus
        if data['method_count'] > 1:
            data['score'] *= (1 + data['method_count'] * 0.15)
        
        final_score = min(data['score'], 95)
        combined_reason = f"Cycle analysis ({data['method_count']} methods)"
        
        final_predictions.append((num, final_score, combined_reason))
    
    return sorted(final_predictions, key=lambda x: x[1], reverse=True)