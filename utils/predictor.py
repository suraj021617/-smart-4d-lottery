import pandas as pd
import re
from collections import Counter

def extract_4d_numbers(df):
    """Extract 4D numbers from CSV data"""
    numbers = []
    for col in ['1st_real', '2nd_real', '3rd_real']:
        if col in df.columns:
            for val in df[col].astype(str):
                matches = re.findall(r'\d{4}', val)
                numbers.extend([m for m in matches if len(m) == 4])
    return numbers

def frequency_predictor(df, top_n=5):
    """Basic frequency-based predictor"""
    numbers = extract_4d_numbers(df)
    if not numbers:
        return []
    
    freq = Counter(numbers)
    return [(num, count) for num, count in freq.most_common(top_n)]

def hot_cold_analysis(df, days=30):
    """Analyze hot and cold numbers"""
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    recent = df[df['date_parsed'] >= cutoff] if 'date_parsed' in df.columns else df.tail(days)
    
    numbers = extract_4d_numbers(recent)
    freq = Counter(numbers)
    
    hot = freq.most_common(10)
    cold = freq.most_common()[-10:] if len(freq) >= 10 else []
    
    return {'hot': hot, 'cold': cold}