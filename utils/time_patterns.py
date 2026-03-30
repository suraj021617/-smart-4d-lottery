"""Time-Based Pattern Analysis"""
import pandas as pd
from collections import Counter

def analyze_time_patterns(df, provider=None):
    """Analyze patterns by day of week, month, etc."""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered['day_of_week'] = df_filtered['date_parsed'].dt.day_name()
    df_filtered['month'] = df_filtered['date_parsed'].dt.month
    df_filtered['day_of_month'] = df_filtered['date_parsed'].dt.day
    
    # Day of week patterns
    dow_patterns = {}
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        day_data = df_filtered[df_filtered['day_of_week'] == day]
        numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            nums = day_data[col].astype(str)
            numbers.extend([n for n in nums if n.isdigit() and len(n) == 4])
        
        if numbers:
            dow_patterns[day] = {
                'count': len(numbers),
                'top_numbers': Counter(numbers).most_common(5)
            }
    
    # Month patterns
    month_patterns = {}
    for month in range(1, 13):
        month_data = df_filtered[df_filtered['month'] == month]
        numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            nums = month_data[col].astype(str)
            numbers.extend([n for n in nums if n.isdigit() and len(n) == 4])
        
        if numbers:
            month_patterns[month] = {
                'count': len(numbers),
                'top_numbers': Counter(numbers).most_common(5)
            }
    
    return {
        'day_of_week': dow_patterns,
        'month': month_patterns
    }

def predict_by_time(df, provider=None, target_date=None):
    """Predict based on time patterns"""
    if target_date is None:
        target_date = pd.Timestamp.now()
    
    patterns = analyze_time_patterns(df, provider)
    
    day_name = target_date.strftime('%A')
    month = target_date.month
    
    predictions = []
    
    # Get numbers from matching day
    if day_name in patterns['day_of_week']:
        predictions.extend([num for num, _ in patterns['day_of_week'][day_name]['top_numbers']])
    
    # Get numbers from matching month
    if month in patterns['month']:
        predictions.extend([num for num, _ in patterns['month'][month]['top_numbers']])
    
    # Return unique predictions
    return list(dict.fromkeys(predictions))[:10]
