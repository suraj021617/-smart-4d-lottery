"""
Prediction Runner Module
Orchestrates all prediction engines with separate button logic
"""
from datetime import datetime
import pandas as pd

from .active_data_filter import (
    get_recent_100_data,
    get_recent_300_data,
    get_last_3y_data,
    get_last_5y_data,
    get_full_history_data
)
from .advanced_predictor import predict_recent_stats
from .ml_predictor import predict_ml_mode
from .ai_predictor import predict_ai_pattern
from .consensus import generate_final_consensus, predict_smart_auto_learn

def run_all_predictions(df, target_date, provider='All'):
    """
    Run all prediction engines for a target date
    
    ANTI-LEAKAGE: Only uses data before target_date
    
    Args:
        df: Full history dataframe
        target_date: Target prediction date
        provider: Lottery provider filter
    
    Returns:
        Dict with all predictions and metadata
    """
    target_date = pd.to_datetime(target_date)
    
    print(f"\n=== Running Predictions for {target_date.strftime('%Y-%m-%d')} ===")
    
    # Get data used until date (last date before target)
    from .history_loader import get_data_until_date
    past_data = get_data_until_date(df, target_date, exclude_target=True)
    
    if len(past_data) == 0:
        return {
            'error': 'No historical data available before target date',
            'target_date': str(target_date),
            'data_used_until': None
        }
    
    data_used_until = past_data['date'].max()
    
    print(f"Data used until: {data_used_until.strftime('%Y-%m-%d')}")
    print(f"Total records: {len(past_data)}")
    
    # Run each predictor with appropriate data window
    all_predictions = {}
    
    # 1. Recent Stats (100-300 draws)
    print("\n1. Running Recent Stats Predictor...")
    recent_data = get_recent_300_data(df, target_date)
    all_predictions['recent_stats'] = predict_recent_stats(recent_data, top_n=5)
    
    # 2. Last 3 Years
    print("2. Running Last 3 Years Predictor...")
    last_3y_data = get_last_3y_data(df, target_date)
    all_predictions['last_3y'] = predict_recent_stats(last_3y_data, top_n=5)
    
    # 3. Last 5 Years (Default Active Dataset)
    print("3. Running Last 5 Years Predictor...")
    last_5y_data = get_last_5y_data(df, target_date)
    all_predictions['last_5y'] = predict_recent_stats(last_5y_data, top_n=5)
    
    # 4. ML Predictor
    print("4. Running ML Predictor...")
    ml_data = last_5y_data  # Use 5-year data for ML
    all_predictions['ml'] = predict_ml_mode(ml_data, top_n=5)
    
    # 5. AI Pattern Predictor
    print("5. Running AI Pattern Predictor...")
    ai_data = last_5y_data  # Use 5-year data for AI
    all_predictions['ai_pattern'] = predict_ai_pattern(ai_data, top_n=5)
    
    # 6. Full History Analysis (reference only)
    print("6. Running Full History Analysis...")
    full_data = get_full_history_data(df, target_date)
    all_predictions['full_history'] = predict_recent_stats(full_data, top_n=5)
    
    # 7. Generate Final Consensus
    print("7. Generating Final Consensus...")
    final_consensus = generate_final_consensus(all_predictions, top_n=5)
    
    # 8. Smart Auto-Learn (same as consensus but explicitly named)
    all_predictions['smart_auto_learn'] = final_consensus
    
    print("\n✓ All predictions complete")
    
    return {
        'target_date': str(target_date),
        'provider': provider,
        'data_used_until': str(data_used_until),
        'predictions': all_predictions,
        'final_consensus': final_consensus,
        'timestamp': datetime.now().isoformat()
    }

def predict_recent_stats_only(df, target_date, top_n=5):
    """Run only recent stats predictor (Button 1)"""
    recent_data = get_recent_300_data(df, target_date)
    return predict_recent_stats(recent_data, top_n)

def predict_last_3_years_only(df, target_date, top_n=5):
    """Run only last 3 years predictor (Button 2)"""
    last_3y_data = get_last_3y_data(df, target_date)
    return predict_recent_stats(last_3y_data, top_n)

def predict_last_5_years_only(df, target_date, top_n=5):
    """Run only last 5 years predictor (Button 3)"""
    last_5y_data = get_last_5y_data(df, target_date)
    return predict_recent_stats(last_5y_data, top_n)

def predict_ml_only(df, target_date, top_n=5):
    """Run only ML predictor (Button 4)"""
    ml_data = get_last_5y_data(df, target_date)
    return predict_ml_mode(ml_data, top_n)

def predict_ai_pattern_only(df, target_date, top_n=5):
    """Run only AI pattern predictor (Button 5)"""
    ai_data = get_last_5y_data(df, target_date)
    return predict_ai_pattern(ai_data, top_n)

def predict_smart_auto_learn_only(df, target_date, top_n=5):
    """Run smart auto-learn predictor (Button 6)"""
    # Run all predictors and generate consensus
    result = run_all_predictions(df, target_date)
    return result.get('final_consensus', [])

def predict_full_history_only(df, target_date, top_n=5):
    """Run full history analysis (Button 7)"""
    full_data = get_full_history_data(df, target_date)
    return predict_recent_stats(full_data, top_n)

def format_predictions_for_display(predictions, show_top_n=5):
    """Format predictions for clean UI display"""
    if not predictions:
        return []
    
    display_list = []
    for i, pred in enumerate(predictions[:show_top_n], 1):
        display_list.append({
            'rank': i,
            'number': pred['number'],
            'score': f"{pred['score']:.1f}",
            'method': pred.get('method', 'unknown')
        })
    
    return display_list
