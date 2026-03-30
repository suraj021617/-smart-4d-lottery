"""Real-Time Odds Calculator"""
import pandas as pd
from collections import Counter
import math

def calculate_odds(df, provider=None, lookback=500):
    """Calculate real-time odds for each 4D number"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered = df_filtered.tail(lookback)
    
    # Count all winning numbers
    all_winners = []
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        nums = df_filtered[col].astype(str)
        all_winners.extend([n for n in nums if n.isdigit() and len(n) == 4])
    
    total_draws = len(df_filtered)
    winner_counts = Counter(all_winners)
    
    # Calculate odds for each number
    odds_data = []
    for num, count in winner_counts.most_common(100):
        frequency = count / total_draws if total_draws > 0 else 0
        probability = frequency * 100
        
        # Calculate implied odds (1 in X chance)
        if frequency > 0:
            implied_odds = 1 / frequency
        else:
            implied_odds = 10000
        
        odds_data.append({
            'number': num,
            'appearances': count,
            'frequency': round(frequency, 4),
            'probability': round(probability, 2),
            'odds': f'1 in {int(implied_odds)}',
            'last_seen': None  # Will be filled below
        })
    
    # Find last appearance for top numbers
    for item in odds_data[:50]:
        num = item['number']
        for idx in range(len(df_filtered)-1, -1, -1):
            row = df_filtered.iloc[idx]
            for col in ['number_1st', 'number_2nd', 'number_3rd']:
                if str(row[col]) == num:
                    item['last_seen'] = row['date_parsed'].strftime('%Y-%m-%d')
                    break
            if item['last_seen']:
                break
    
    return odds_data

def calculate_number_probability(df, number, provider=None, lookback=500):
    """Calculate probability for a specific number"""
    df_filtered = df.copy()
    if provider and provider != 'all':
        df_filtered = df_filtered[df_filtered['provider_key'] == provider]
    
    df_filtered = df_filtered.tail(lookback)
    
    # Count appearances
    count = 0
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        count += (df_filtered[col].astype(str) == str(number)).sum()
    
    total_draws = len(df_filtered)
    
    if total_draws == 0:
        return 0
    
    probability = (count / total_draws) * 100
    
    return {
        'number': number,
        'appearances': count,
        'total_draws': total_draws,
        'probability': round(probability, 2),
        'odds': f'1 in {int(total_draws/count) if count > 0 else 10000}'
    }

def predict_with_odds(predictions, odds_data):
    """Enhance predictions with odds information"""
    odds_dict = {item['number']: item for item in odds_data}
    
    enhanced = []
    for pred in predictions:
        if isinstance(pred, tuple):
            num, score, reason = pred
        else:
            num = pred
            score = 0.5
            reason = 'Prediction'
        
        odds_info = odds_dict.get(num, {})
        
        # Adjust score based on odds
        if odds_info:
            prob = odds_info.get('probability', 0)
            adjusted_score = (score * 0.7) + (prob / 100 * 0.3)
        else:
            adjusted_score = score * 0.5  # Penalize numbers never seen
        
        enhanced.append((
            num,
            min(adjusted_score, 0.99),
            f"{reason} | Odds: {odds_info.get('odds', 'Unknown')}"
        ))
    
    return sorted(enhanced, key=lambda x: x[1], reverse=True)
