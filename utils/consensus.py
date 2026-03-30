"""
Consensus Module
Merges predictions from all engines with adaptive weighting
"""
import json
import os
from collections import defaultdict

# Default weights (will be updated by auto-learning)
DEFAULT_WEIGHTS = {
    'recent_stats': 1.0,
    'last_3y': 1.0,
    'last_5y': 1.2,  # Slightly higher as it's the default active dataset
    'ml': 1.0,
    'ai_pattern': 1.0,
    'full_history': 0.8  # Lower weight as it's for reference only
}

def load_current_weights():
    """Load current adaptive weights from file"""
    weights_file = 'model_weights.json'
    
    if os.path.exists(weights_file):
        try:
            with open(weights_file, 'r') as f:
                weights = json.load(f)
                return weights
        except:
            pass
    
    return DEFAULT_WEIGHTS.copy()

def save_weights(weights):
    """Save updated weights to file"""
    weights_file = 'model_weights.json'
    with open(weights_file, 'w') as f:
        json.dump(weights, f, indent=2)

def generate_final_consensus(all_predictions, top_n=5):
    """
    Generate final consensus from all predictor outputs
    
    Args:
        all_predictions: Dict with keys like 'recent_stats', 'ml', etc.
                        Each value is a list of prediction dicts with 'number' and 'score'
        top_n: Number of final predictions to return
    
    Returns:
        List of top N consensus predictions with scores
    """
    # Load current weights
    weights = load_current_weights()
    
    # Aggregate scores for each number
    number_scores = defaultdict(lambda: {
        'total_score': 0.0,
        'predictor_count': 0,
        'predictors': [],
        'raw_scores': {}
    })
    
    for predictor_name, predictions in all_predictions.items():
        if predictions is None or len(predictions) == 0:
            continue
        
        weight = weights.get(predictor_name, 1.0)
        
        for pred in predictions:
            number = pred['number']
            score = pred['score']
            
            # Weighted score
            weighted_score = score * weight
            
            number_scores[number]['total_score'] += weighted_score
            number_scores[number]['predictor_count'] += 1
            number_scores[number]['predictors'].append(predictor_name)
            number_scores[number]['raw_scores'][predictor_name] = score
    
    # Convert to list and calculate consensus score
    consensus_list = []
    for number, data in number_scores.items():
        # Consensus score = weighted average + bonus for multiple predictors
        avg_score = data['total_score'] / max(1, data['predictor_count'])
        consensus_bonus = data['predictor_count'] * 10  # Bonus for agreement
        
        final_score = avg_score + consensus_bonus
        
        consensus_list.append({
            'number': number,
            'score': final_score,
            'consensus_score': final_score,
            'predictor_count': data['predictor_count'],
            'predictors': data['predictors'],
            'raw_scores': data['raw_scores'],
            'method': 'consensus'
        })
    
    # Sort by consensus score
    consensus_list.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top N
    return consensus_list[:top_n]

def predict_smart_auto_learn(all_predictions, top_n=5):
    """
    Smart auto-learn predictor (alias for consensus with current weights)
    This uses adaptive weights that are updated after each evaluation
    """
    return generate_final_consensus(all_predictions, top_n)

def get_current_weights():
    """Get current predictor weights"""
    return load_current_weights()

def explain_prediction(prediction):
    """Generate explanation for why a prediction was ranked highly"""
    explanations = []
    
    if prediction['predictor_count'] > 1:
        explanations.append(f"Agreed by {prediction['predictor_count']} predictors")
    
    if 'predictors' in prediction:
        predictor_names = ', '.join(prediction['predictors'])
        explanations.append(f"Supported by: {predictor_names}")
    
    if 'consensus_score' in prediction:
        explanations.append(f"Consensus score: {prediction['consensus_score']:.1f}")
    
    return ' | '.join(explanations)
