"""
Drift Analyzer Module
Detects recent changes and trends in lottery patterns
"""
import pandas as pd
import numpy as np
from collections import Counter

def analyze_recent_drift(df, target_date, recent_window=100, baseline_window=500):
    """
    Analyze drift between recent data and baseline
    
    Detects:
    - Digit frequency shifts
    - Hot/cold digit changes
    - Pair/triple pattern changes
    - Sum range changes
    - Odd/even ratio changes
    - Positional digit changes
    
    Args:
        df: Full history dataframe
        target_date: Target date for analysis
        recent_window: Recent draws to analyze
        baseline_window: Baseline draws for comparison
    
    Returns:
        Drift analysis report dict
    """
    from .active_data_filter import get_recent_n_draws
    from .history_loader import get_data_until_date
    
    # Get data before target date
    past_data = get_data_until_date(df, target_date, exclude_target=True)
    
    if len(past_data) < recent_window + baseline_window:
        return {'error': 'Insufficient data for drift analysis'}
    
    # Get recent and baseline data
    recent_data = get_recent_n_draws(past_data, target_date, n=recent_window)
    baseline_data = get_recent_n_draws(past_data, target_date, n=baseline_window)
    
    # Exclude recent from baseline
    baseline_dates = baseline_data['date'].unique()
    recent_dates = recent_data['date'].unique()
    baseline_only_dates = [d for d in baseline_dates if d not in recent_dates]
    baseline_data = baseline_data[baseline_data['date'].isin(baseline_only_dates)]
    
    drift_report = {
        'recent_window': recent_window,
        'baseline_window': baseline_window,
        'digit_frequency_drift': analyze_digit_drift(recent_data, baseline_data),
        'hot_cold_drift': analyze_hot_cold_drift(recent_data, baseline_data),
        'sum_drift': analyze_sum_drift(recent_data, baseline_data),
        'odd_even_drift': analyze_odd_even_drift(recent_data, baseline_data),
        'positional_drift': analyze_positional_drift(recent_data, baseline_data),
        'pair_drift': analyze_pair_drift(recent_data, baseline_data)
    }
    
    # Calculate overall drift score
    drift_report['overall_drift_score'] = calculate_overall_drift(drift_report)
    
    return drift_report

def analyze_digit_drift(recent_data, baseline_data):
    """Analyze digit frequency drift"""
    recent_digits = []
    baseline_digits = []
    
    for num in recent_data['number']:
        recent_digits.extend(list(str(num).zfill(4)))
    
    for num in baseline_data['number']:
        baseline_digits.extend(list(str(num).zfill(4)))
    
    recent_freq = Counter(recent_digits)
    baseline_freq = Counter(baseline_digits)
    
    # Normalize to percentages
    recent_total = sum(recent_freq.values())
    baseline_total = sum(baseline_freq.values())
    
    drift = {}
    for digit in '0123456789':
        recent_pct = (recent_freq.get(digit, 0) / recent_total * 100) if recent_total > 0 else 0
        baseline_pct = (baseline_freq.get(digit, 0) / baseline_total * 100) if baseline_total > 0 else 0
        
        drift[digit] = {
            'recent': recent_pct,
            'baseline': baseline_pct,
            'change': recent_pct - baseline_pct
        }
    
    return drift

def analyze_hot_cold_drift(recent_data, baseline_data):
    """Analyze hot/cold digit changes"""
    recent_freq = Counter()
    baseline_freq = Counter()
    
    for num in recent_data['number']:
        for digit in str(num).zfill(4):
            recent_freq[digit] += 1
    
    for num in baseline_data['number']:
        for digit in str(num).zfill(4):
            baseline_freq[digit] += 1
    
    recent_hot = [d for d, _ in recent_freq.most_common(5)]
    baseline_hot = [d for d, _ in baseline_freq.most_common(5)]
    
    recent_cold = [d for d, _ in recent_freq.most_common()[-5:]]
    baseline_cold = [d for d, _ in baseline_freq.most_common()[-5:]]
    
    return {
        'recent_hot': recent_hot,
        'baseline_hot': baseline_hot,
        'hot_changed': len(set(recent_hot) - set(baseline_hot)),
        'recent_cold': recent_cold,
        'baseline_cold': baseline_cold,
        'cold_changed': len(set(recent_cold) - set(baseline_cold))
    }

def analyze_sum_drift(recent_data, baseline_data):
    """Analyze digit sum distribution drift"""
    recent_sums = []
    baseline_sums = []
    
    for num in recent_data['number']:
        digit_sum = sum(int(d) for d in str(num).zfill(4))
        recent_sums.append(digit_sum)
    
    for num in baseline_data['number']:
        digit_sum = sum(int(d) for d in str(num).zfill(4))
        baseline_sums.append(digit_sum)
    
    return {
        'recent_mean': np.mean(recent_sums),
        'baseline_mean': np.mean(baseline_sums),
        'recent_std': np.std(recent_sums),
        'baseline_std': np.std(baseline_sums),
        'mean_change': np.mean(recent_sums) - np.mean(baseline_sums)
    }

def analyze_odd_even_drift(recent_data, baseline_data):
    """Analyze odd/even ratio drift"""
    def count_odd_even(data):
        odd_count = 0
        even_count = 0
        
        for num in data['number']:
            for digit in str(num).zfill(4):
                if int(digit) % 2 == 1:
                    odd_count += 1
                else:
                    even_count += 1
        
        total = odd_count + even_count
        return {
            'odd_ratio': odd_count / total if total > 0 else 0,
            'even_ratio': even_count / total if total > 0 else 0
        }
    
    recent_ratio = count_odd_even(recent_data)
    baseline_ratio = count_odd_even(baseline_data)
    
    return {
        'recent_odd_ratio': recent_ratio['odd_ratio'],
        'baseline_odd_ratio': baseline_ratio['odd_ratio'],
        'odd_ratio_change': recent_ratio['odd_ratio'] - baseline_ratio['odd_ratio']
    }

def analyze_positional_drift(recent_data, baseline_data):
    """Analyze positional digit distribution drift"""
    def get_positional_freq(data):
        pos_freq = [Counter(), Counter(), Counter(), Counter()]
        
        for num in data['number']:
            num_str = str(num).zfill(4)
            for i, digit in enumerate(num_str):
                pos_freq[i][digit] += 1
        
        return pos_freq
    
    recent_pos = get_positional_freq(recent_data)
    baseline_pos = get_positional_freq(baseline_data)
    
    drift = {}
    for i in range(4):
        recent_top = [d for d, _ in recent_pos[i].most_common(3)]
        baseline_top = [d for d, _ in baseline_pos[i].most_common(3)]
        
        drift[f'position_{i}'] = {
            'recent_top': recent_top,
            'baseline_top': baseline_top,
            'changed': len(set(recent_top) - set(baseline_top))
        }
    
    return drift

def analyze_pair_drift(recent_data, baseline_data):
    """Analyze pair frequency drift"""
    def get_pair_freq(data):
        pairs = []
        for num in data['number']:
            num_str = str(num).zfill(4)
            for i in range(len(num_str) - 1):
                pairs.append(num_str[i:i+2])
        return Counter(pairs)
    
    recent_pairs = get_pair_freq(recent_data)
    baseline_pairs = get_pair_freq(baseline_data)
    
    recent_top = [p for p, _ in recent_pairs.most_common(10)]
    baseline_top = [p for p, _ in baseline_pairs.most_common(10)]
    
    return {
        'recent_top_pairs': recent_top,
        'baseline_top_pairs': baseline_top,
        'pairs_changed': len(set(recent_top) - set(baseline_top))
    }

def calculate_overall_drift(drift_report):
    """Calculate overall drift score (0-100)"""
    score = 0.0
    
    # Digit frequency drift
    digit_drift = drift_report['digit_frequency_drift']
    avg_digit_change = np.mean([abs(d['change']) for d in digit_drift.values()])
    score += avg_digit_change * 2
    
    # Hot/cold drift
    hot_cold = drift_report['hot_cold_drift']
    score += hot_cold['hot_changed'] * 5
    score += hot_cold['cold_changed'] * 3
    
    # Sum drift
    sum_drift = drift_report['sum_drift']
    score += abs(sum_drift['mean_change']) * 2
    
    # Odd/even drift
    odd_even = drift_report['odd_even_drift']
    score += abs(odd_even['odd_ratio_change']) * 50
    
    # Positional drift
    pos_drift = drift_report['positional_drift']
    total_pos_changes = sum(p['changed'] for p in pos_drift.values())
    score += total_pos_changes * 3
    
    # Pair drift
    pair_drift = drift_report['pair_drift']
    score += pair_drift['pairs_changed'] * 2
    
    return min(100, score)

def format_drift_report(drift_report):
    """Format drift report as readable text"""
    if 'error' in drift_report:
        return f"Error: {drift_report['error']}"
    
    report = []
    report.append("=== DRIFT ANALYSIS REPORT ===")
    report.append(f"Overall Drift Score: {drift_report['overall_drift_score']:.1f}/100")
    report.append("")
    
    # Hot/cold changes
    hot_cold = drift_report['hot_cold_drift']
    report.append(f"Hot Digits Changed: {hot_cold['hot_changed']}/5")
    report.append(f"Recent Hot: {', '.join(hot_cold['recent_hot'])}")
    report.append("")
    
    # Sum drift
    sum_drift = drift_report['sum_drift']
    report.append(f"Sum Mean Change: {sum_drift['mean_change']:+.2f}")
    report.append(f"Recent: {sum_drift['recent_mean']:.2f}, Baseline: {sum_drift['baseline_mean']:.2f}")
    report.append("")
    
    # Odd/even drift
    odd_even = drift_report['odd_even_drift']
    report.append(f"Odd Ratio Change: {odd_even['odd_ratio_change']:+.3f}")
    report.append("")
    
    return '\n'.join(report)
