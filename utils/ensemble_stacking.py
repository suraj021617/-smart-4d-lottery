"""Ensemble Stacking - Combines multiple predictors intelligently"""
import numpy as np
from collections import Counter

def ensemble_stack(predictions_dict, weights=None):
    """
    Stack multiple prediction methods with intelligent weighting
    
    predictions_dict: {
        'method1': [(num, score, reason), ...],
        'method2': [(num, score, reason), ...],
        ...
    }
    """
    if weights is None:
        # Default equal weights
        weights = {method: 1.0 for method in predictions_dict.keys()}
    
    # Collect all predictions with weighted scores
    weighted_scores = {}
    method_votes = {}
    
    for method, preds in predictions_dict.items():
        weight = weights.get(method, 1.0)
        
        for num, score, reason in preds:
            if num not in weighted_scores:
                weighted_scores[num] = 0
                method_votes[num] = []
            
            weighted_scores[num] += score * weight
            method_votes[num].append(method)
    
    # Calculate ensemble score
    ensemble_predictions = []
    for num, total_score in weighted_scores.items():
        # Normalize by number of methods that voted
        num_votes = len(method_votes[num])
        avg_score = total_score / sum(weights.values())
        
        # Boost score if multiple methods agree
        consensus_boost = min(num_votes * 0.1, 0.3)
        final_score = min(avg_score + consensus_boost, 0.99)
        
        methods_str = ', '.join(method_votes[num])
        reason = f'Ensemble: {methods_str} ({num_votes} votes)'
        
        ensemble_predictions.append((num, final_score, reason))
    
    # Sort by score
    ensemble_predictions.sort(key=lambda x: x[1], reverse=True)
    
    return ensemble_predictions[:10]

def adaptive_weights(accuracy_history):
    """
    Calculate adaptive weights based on historical accuracy
    
    accuracy_history: {
        'method1': accuracy_percentage,
        'method2': accuracy_percentage,
        ...
    }
    """
    if not accuracy_history:
        return None
    
    # Normalize accuracies to weights
    total_accuracy = sum(accuracy_history.values())
    
    if total_accuracy == 0:
        return {method: 1.0 for method in accuracy_history.keys()}
    
    weights = {
        method: acc / total_accuracy * len(accuracy_history)
        for method, acc in accuracy_history.items()
    }
    
    return weights

def meta_ensemble(df, provider=None, lookback=200):
    """Meta-ensemble that combines all available predictors"""
    from utils.advanced_predictor import advanced_predictor
    from utils.smart_auto_weight import smart_auto_weight_predictor
    from utils.ml_predictor import ml_predictor
    from utils.lstm_predictor import lstm_predict
    
    predictions = {}
    
    try:
        predictions['advanced'] = advanced_predictor(df, provider, lookback) or []
    except:
        predictions['advanced'] = []
    
    try:
        predictions['smart'] = smart_auto_weight_predictor(df, provider, lookback) or []
    except:
        predictions['smart'] = []
    
    try:
        predictions['ml'] = ml_predictor(df, lookback) or []
    except:
        predictions['ml'] = []
    
    try:
        predictions['lstm'] = lstm_predict(df, provider, lookback) or []
    except:
        predictions['lstm'] = []
    
    # Use adaptive weights if available
    weights = {
        'advanced': 1.0,
        'smart': 1.2,
        'ml': 1.1,
        'lstm': 0.9
    }
    
    return ensemble_stack(predictions, weights)
