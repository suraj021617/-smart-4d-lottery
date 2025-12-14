"""
Advanced Data Features for Lottery Prediction
"""
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re

def extract_advanced_features(df):
    """Extract advanced statistical features from lottery data"""
    features = {}
    
    # 1. Temporal Features
    df['hour'] = df['date_parsed'].dt.hour
    df['day_of_week'] = df['date_parsed'].dt.dayofweek
    df['month'] = df['date_parsed'].dt.month
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    
    # 2. Number Pattern Features
    all_numbers = []
    for col in ['1st_real', '2nd_real', '3rd_real']:
        if col in df.columns:
            all_numbers.extend([n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    # Digital root analysis
    digital_roots = [sum(int(d) for d in num) % 9 or 9 for num in all_numbers]
    features['digital_root_dist'] = Counter(digital_roots)
    
    # Sum range analysis
    number_sums = [sum(int(d) for d in num) for num in all_numbers]
    features['sum_ranges'] = {
        'low': len([s for s in number_sums if s <= 15]),
        'medium': len([s for s in number_sums if 16 <= s <= 25]),
        'high': len([s for s in number_sums if s >= 26])
    }
    
    # 3. Sequence Detection
    features['sequences'] = detect_number_sequences(all_numbers)
    
    # 4. Gap Analysis
    features['gaps'] = analyze_number_gaps(df, all_numbers)
    
    return features

def detect_number_sequences(numbers):
    """Detect mathematical sequences in numbers"""
    sequences = {
        'consecutive': 0,
        'arithmetic': 0,
        'fibonacci': 0,
        'prime_clusters': 0
    }
    
    primes = {2, 3, 5, 7}
    fib = [1, 1, 2, 3, 5, 8]
    
    for num in numbers:
        digits = [int(d) for d in num]
        
        # Consecutive digits
        if all(digits[i] + 1 == digits[i+1] for i in range(3)):
            sequences['consecutive'] += 1
        
        # Arithmetic progression
        if len(set(digits[i+1] - digits[i] for i in range(3))) == 1:
            sequences['arithmetic'] += 1
        
        # Prime clustering
        prime_count = sum(1 for d in digits if d in primes)
        if prime_count >= 3:
            sequences['prime_clusters'] += 1
    
    return sequences

def analyze_number_gaps(df, numbers):
    """Analyze gaps between number appearances"""
    gaps = {}
    number_positions = defaultdict(list)
    
    # Track positions of each number
    for i, num in enumerate(numbers):
        number_positions[num].append(i)
    
    # Calculate gaps
    for num, positions in number_positions.items():
        if len(positions) > 1:
            gaps[num] = [positions[i] - positions[i-1] for i in range(1, len(positions))]
    
    return gaps

def calculate_momentum_indicators(df):
    """Calculate momentum indicators for numbers"""
    momentum = {}
    
    # Recent vs historical frequency
    recent_30 = df.tail(30)
    historical = df.head(-30) if len(df) > 30 else df
    
    recent_nums = []
    historical_nums = []
    
    for col in ['1st_real', '2nd_real', '3rd_real']:
        recent_nums.extend([n for n in recent_30[col].astype(str) if len(n) == 4 and n.isdigit()])
        historical_nums.extend([n for n in historical[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    recent_freq = Counter(recent_nums)
    historical_freq = Counter(historical_nums)
    
    for num in set(recent_nums + historical_nums):
        recent_rate = recent_freq.get(num, 0) / len(recent_nums) if recent_nums else 0
        historical_rate = historical_freq.get(num, 0) / len(historical_nums) if historical_nums else 0
        
        if historical_rate > 0:
            momentum[num] = recent_rate / historical_rate
        else:
            momentum[num] = recent_rate * 10  # Boost for new numbers
    
    return momentum

def detect_cyclical_patterns(df):
    """Detect cyclical patterns in lottery draws"""
    cycles = {}
    
    # Weekly cycles
    weekly_patterns = df.groupby(df['date_parsed'].dt.dayofweek).size()
    cycles['weekly'] = weekly_patterns.to_dict()
    
    # Monthly cycles
    monthly_patterns = df.groupby(df['date_parsed'].dt.day).size()
    cycles['monthly'] = monthly_patterns.to_dict()
    
    return cycles

def analyze_provider_synchronization(df):
    """Analyze synchronization patterns between providers"""
    sync_data = {}
    providers = df['provider'].unique()
    
    for provider in providers:
        if not provider or str(provider).strip() == '':
            continue
            
        provider_df = df[df['provider'] == provider]
        provider_nums = []
        
        for col in ['1st_real', '2nd_real', '3rd_real']:
            provider_nums.extend([n for n in provider_df[col].astype(str) if len(n) == 4 and n.isdigit()])
        
        sync_data[provider] = {
            'unique_numbers': len(set(provider_nums)),
            'total_draws': len(provider_df),
            'diversity_score': len(set(provider_nums)) / len(provider_nums) if provider_nums else 0
        }
    
    return sync_data