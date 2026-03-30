"""
Result Evaluator Module
Evaluates prediction accuracy after actual results are known
"""
import json
import os
from datetime import datetime
import pandas as pd

EVALUATION_LOG_FILE = 'evaluation_logs.jsonl'

def evaluate_after_result(log_id, actual_result):
    """
    Evaluate predictions after actual result is known
    
    Args:
        log_id: Prediction log ID
        actual_result: Actual winning number (4 digits)
    
    Returns:
        Evaluation results dict
    """
    from .prediction_logger import load_prediction_log
    
    # Load the prediction log
    pred_log = load_prediction_log(log_id)
    
    if not pred_log:
        print(f"✗ Prediction log not found: {log_id}")
        return None
    
    # Normalize actual result
    actual_result = str(actual_result).zfill(4)
    
    # Evaluate each predictor
    evaluation = {
        'log_id': log_id,
        'target_date': pred_log['target_date'],
        'provider': pred_log['provider'],
        'actual_result': actual_result,
        'timestamp_evaluated': datetime.now().isoformat(),
        'predictor_results': {}
    }
    
    for engine_name, predictions in pred_log['predictions'].items():
        engine_eval = evaluate_predictor(predictions, actual_result)
        evaluation['predictor_results'][engine_name] = engine_eval
    
    # Save evaluation
    with open(EVALUATION_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(evaluation) + '\n')
    
    print(f"✓ Evaluation saved: {log_id}")
    
    return evaluation

def evaluate_predictor(predictions, actual_result):
    """
    Evaluate a single predictor's performance
    
    Returns:
        Dict with evaluation metrics
    """
    actual_result = str(actual_result).zfill(4)
    
    result = {
        'exact_hit': False,
        'best_match_number': None,
        'best_match_score': 0,
        'positional_matches': {
            '4_digit': 0,
            '3_digit': 0,
            '2_digit': 0,
            '1_digit': 0
        },
        'top_5_predictions': []
    }
    
    best_score = 0
    best_number = None
    
    for pred in predictions[:5]:  # Check top 5
        pred_number = str(pred['number']).zfill(4)
        result['top_5_predictions'].append(pred_number)
        
        # Check exact match
        if pred_number == actual_result:
            result['exact_hit'] = True
            result['best_match_number'] = pred_number
            result['best_match_score'] = 4
            result['positional_matches']['4_digit'] = 1
            return result
        
        # Calculate positional match score
        match_score = calculate_match_score(pred_number, actual_result)
        
        if match_score > best_score:
            best_score = match_score
            best_number = pred_number
    
    result['best_match_number'] = best_number
    result['best_match_score'] = best_score
    
    # Count positional matches for best prediction
    if best_number:
        if best_score == 3:
            result['positional_matches']['3_digit'] = 1
        elif best_score == 2:
            result['positional_matches']['2_digit'] = 1
        elif best_score == 1:
            result['positional_matches']['1_digit'] = 1
    
    return result

def calculate_match_score(predicted, actual):
    """
    Calculate positional match score (0-4)
    
    Returns:
        Number of digits matching in correct position
    """
    predicted = str(predicted).zfill(4)
    actual = str(actual).zfill(4)
    
    matches = sum(1 for p, a in zip(predicted, actual) if p == a)
    return matches

def load_all_evaluations():
    """Load all evaluation logs"""
    evaluations = []
    
    if not os.path.exists(EVALUATION_LOG_FILE):
        return evaluations
    
    with open(EVALUATION_LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                evaluations.append(entry)
            except:
                continue
    
    return evaluations

def get_predictor_leaderboard(recent_n=50):
    """
    Get predictor performance leaderboard
    
    Args:
        recent_n: Number of recent evaluations to consider
    
    Returns:
        Dict with predictor performance stats
    """
    evaluations = load_all_evaluations()
    
    # Take most recent N evaluations
    evaluations = evaluations[-recent_n:] if len(evaluations) > recent_n else evaluations
    
    leaderboard = {}
    
    for eval_entry in evaluations:
        for predictor_name, result in eval_entry['predictor_results'].items():
            if predictor_name not in leaderboard:
                leaderboard[predictor_name] = {
                    'total_predictions': 0,
                    'exact_hits': 0,
                    '3_digit_matches': 0,
                    '2_digit_matches': 0,
                    '1_digit_matches': 0,
                    'total_match_score': 0,
                    'avg_match_score': 0.0
                }
            
            stats = leaderboard[predictor_name]
            stats['total_predictions'] += 1
            
            if result['exact_hit']:
                stats['exact_hits'] += 1
            
            stats['3_digit_matches'] += result['positional_matches']['3_digit']
            stats['2_digit_matches'] += result['positional_matches']['2_digit']
            stats['1_digit_matches'] += result['positional_matches']['1_digit']
            
            stats['total_match_score'] += result['best_match_score']
    
    # Calculate averages
    for predictor_name, stats in leaderboard.items():
        if stats['total_predictions'] > 0:
            stats['avg_match_score'] = stats['total_match_score'] / stats['total_predictions']
    
    # Sort by average match score
    sorted_leaderboard = dict(sorted(
        leaderboard.items(),
        key=lambda x: x[1]['avg_match_score'],
        reverse=True
    ))
    
    return sorted_leaderboard

def get_window_performance(recent_n=50):
    """
    Get performance comparison for different time windows
    
    Returns:
        Dict with window performance stats
    """
    leaderboard = get_predictor_leaderboard(recent_n)
    
    window_stats = {}
    
    # Map predictors to windows
    window_mapping = {
        'recent_stats': 'Recent 100-300',
        'last_3y': 'Last 3 Years',
        'last_5y': 'Last 5 Years',
        'full_history': 'Full History'
    }
    
    for predictor_name, stats in leaderboard.items():
        window_name = window_mapping.get(predictor_name, predictor_name)
        window_stats[window_name] = stats
    
    return window_stats

def format_evaluation_report(evaluation):
    """Format evaluation results as readable report"""
    report = []
    report.append(f"Evaluation Report for {evaluation['target_date']}")
    report.append(f"Provider: {evaluation['provider']}")
    report.append(f"Actual Result: {evaluation['actual_result']}")
    report.append("")
    
    for predictor_name, result in evaluation['predictor_results'].items():
        report.append(f"{predictor_name.upper()}:")
        
        if result['exact_hit']:
            report.append(f"  ✓ EXACT HIT!")
        else:
            report.append(f"  Best Match: {result['best_match_number']} (Score: {result['best_match_score']}/4)")
        
        report.append(f"  Top 5: {', '.join(result['top_5_predictions'])}")
        report.append("")
    
    return '\n'.join(report)
