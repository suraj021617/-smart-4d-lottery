"""Overdue Number Tracker"""
import pandas as pd
from collections import defaultdict

def track_overdue_numbers(df, provider=None, lookback=100):
    """Track numbers that haven't appeared recently"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered = df_filtered.tail(lookback)
    
    # Get all winning numbers in recent draws
    recent_winners = set()
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        recent_winners.update([n for n in nums if n.isdigit() and len(n) == 4])
    
    # Get historical numbers (all time)
    all_numbers = set()
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df[col].astype(str)
        all_numbers.update([n for n in nums if n.isdigit() and len(n) == 4])
    
    # Find overdue numbers
    overdue = all_numbers - recent_winners
    
    # Calculate last appearance for each overdue number
    overdue_details = []
    for num in overdue:
        last_seen = None
        for idx, row in df.iterrows():
            for col in ['number_1st', 'number_2nd', 'number_3rd']:
                if str(row[col]) == num:
                    last_seen = row['date_parsed']
                    break
            if last_seen:
                break
        
        if last_seen:
            days_overdue = (pd.Timestamp.now() - last_seen).days
            overdue_details.append((num, days_overdue, last_seen))
    
    # Sort by days overdue
    overdue_details.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'overdue_numbers': overdue_details[:50],
        'total_overdue': len(overdue),
        'lookback_draws': lookback
    }

def get_hot_numbers(df, provider=None, lookback=50):
    """Get frequently appearing numbers (opposite of overdue)"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered = df_filtered.tail(lookback)
    
    numbers = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        numbers.extend([n for n in nums if n.isdigit() and len(n) == 4])
    
    from collections import Counter
    hot = Counter(numbers).most_common(20)
    
    return {
        'hot_numbers': hot,
        'lookback_draws': lookback
    }
