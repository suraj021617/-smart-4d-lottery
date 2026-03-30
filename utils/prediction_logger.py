"""
Prediction Logger Module
Saves prediction snapshots before actual results are known
"""
import json
import os
from datetime import datetime
import pandas as pd

PREDICTION_LOG_FILE = 'prediction_logs.jsonl'

def save_prediction_log(target_date, provider, predictions_dict, weights_used, data_used_until):
    """
    Save prediction snapshot to log file
    
    Args:
        target_date: Target prediction date
        provider: Lottery provider name
        predictions_dict: Dict containing all predictor outputs
        weights_used: Current predictor weights
        data_used_until: Last date of data used for prediction
    
    Returns:
        Log entry ID
    """
    log_entry = {
        'log_id': generate_log_id(target_date, provider),
        'target_date': str(target_date),
        'provider': provider,
        'timestamp_generated': datetime.now().isoformat(),
        'data_used_until': str(data_used_until),
        'weights_used': weights_used,
        'predictions': {}
    }
    
    # Save predictions from each engine
    for engine_name, predictions in predictions_dict.items():
        if predictions:
            log_entry['predictions'][engine_name] = [
                {
                    'number': p['number'],
                    'score': float(p['score']),
                    'method': p.get('method', engine_name)
                }
                for p in predictions[:5]  # Save top 5 from each
            ]
    
    # Append to log file (JSONL format - one JSON per line)
    with open(PREDICTION_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"✓ Prediction logged: {log_entry['log_id']}")
    
    return log_entry['log_id']

def generate_log_id(target_date, provider):
    """Generate unique log ID"""
    date_str = pd.to_datetime(target_date).strftime('%Y%m%d')
    provider_clean = provider.replace(' ', '_').lower()
    return f"{date_str}_{provider_clean}"

def load_prediction_log(log_id):
    """Load a specific prediction log by ID"""
    if not os.path.exists(PREDICTION_LOG_FILE):
        return None
    
    with open(PREDICTION_LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry.get('log_id') == log_id:
                    return entry
            except:
                continue
    
    return None

def load_all_prediction_logs():
    """Load all prediction logs"""
    logs = []
    
    if not os.path.exists(PREDICTION_LOG_FILE):
        return logs
    
    with open(PREDICTION_LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                logs.append(entry)
            except:
                continue
    
    return logs

def get_recent_logs(n=10):
    """Get N most recent prediction logs"""
    logs = load_all_prediction_logs()
    
    # Sort by timestamp
    logs.sort(key=lambda x: x.get('timestamp_generated', ''), reverse=True)
    
    return logs[:n]

def find_log_for_date(target_date, provider=None):
    """Find prediction log for a specific date"""
    logs = load_all_prediction_logs()
    
    target_str = pd.to_datetime(target_date).strftime('%Y-%m-%d')
    
    matching_logs = []
    for log in logs:
        if log.get('target_date', '').startswith(target_str):
            if provider is None or log.get('provider', '').lower() == provider.lower():
                matching_logs.append(log)
    
    return matching_logs

def get_prediction_summary():
    """Get summary of all logged predictions"""
    logs = load_all_prediction_logs()
    
    summary = {
        'total_predictions': len(logs),
        'date_range': None,
        'providers': set(),
        'engines_used': set()
    }
    
    if logs:
        dates = [log.get('target_date', '') for log in logs if log.get('target_date')]
        if dates:
            summary['date_range'] = f"{min(dates)} to {max(dates)}"
        
        for log in logs:
            if 'provider' in log:
                summary['providers'].add(log['provider'])
            if 'predictions' in log:
                summary['engines_used'].update(log['predictions'].keys())
    
    summary['providers'] = list(summary['providers'])
    summary['engines_used'] = list(summary['engines_used'])
    
    return summary
