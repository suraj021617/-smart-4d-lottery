"""
Weight Updater Module
Updates predictor weights based on recent performance (adaptive learning)
"""
import json
from .result_evaluator import get_predictor_leaderboard
from .consensus import load_current_weights, save_weights, DEFAULT_WEIGHTS

def update_weights_after_result(recent_n=20, learning_rate=0.1):
    """
    Update predictor weights based on recent performance
    
    This is the AUTO-LEARNING component that adapts after evaluations
    
    Args:
        recent_n: Number of recent evaluations to consider
        learning_rate: How quickly to adapt (0.0 to 1.0)
    
    Returns:
        Updated weights dict
    """
    # Get current weights
    current_weights = load_current_weights()
    
    # Get recent performance
    leaderboard = get_predictor_leaderboard(recent_n)
    
    if not leaderboard:
        print("No evaluation data available for weight update")
        return current_weights
    
    # Calculate performance scores (0.0 to 1.0)
    performance_scores = {}
    max_score = 0.0
    
    for predictor_name, stats in leaderboard.items():
        # Performance metric: weighted combination of exact hits and match scores
        exact_hit_score = stats['exact_hits'] * 100
        match_score = stats['avg_match_score'] * 25
        
        total_score = exact_hit_score + match_score
        performance_scores[predictor_name] = total_score
        
        if total_score > max_score:
            max_score = total_score
    
    # Normalize scores
    if max_score > 0:
        for predictor_name in performance_scores:
            performance_scores[predictor_name] /= max_score
    
    # Update weights using exponential moving average
    new_weights = {}
    
    for predictor_name in current_weights:
        current_weight = current_weights[predictor_name]
        
        if predictor_name in performance_scores:
            performance = performance_scores[predictor_name]
            
            # Target weight based on performance (0.5 to 1.5 range)
            target_weight = 0.5 + performance * 1.0
            
            # Smooth update using learning rate
            new_weight = current_weight * (1 - learning_rate) + target_weight * learning_rate
            
            # Clamp to reasonable range
            new_weight = max(0.3, min(2.0, new_weight))
            
            new_weights[predictor_name] = new_weight
        else:
            # Keep current weight if no performance data
            new_weights[predictor_name] = current_weight
    
    # Save updated weights
    save_weights(new_weights)
    
    print("✓ Weights updated based on recent performance")
    print_weight_changes(current_weights, new_weights)
    
    return new_weights

def print_weight_changes(old_weights, new_weights):
    """Print weight changes for debugging"""
    print("\nWeight Changes:")
    for predictor_name in new_weights:
        old = old_weights.get(predictor_name, 1.0)
        new = new_weights[predictor_name]
        change = new - old
        
        if abs(change) > 0.01:
            direction = "↑" if change > 0 else "↓"
            print(f"  {predictor_name}: {old:.3f} → {new:.3f} {direction}")

def reset_weights_to_default():
    """Reset weights to default values"""
    save_weights(DEFAULT_WEIGHTS.copy())
    print("✓ Weights reset to default")
    return DEFAULT_WEIGHTS.copy()

def get_weight_history():
    """Get history of weight changes (if tracked)"""
    # This could be extended to track weight changes over time
    # For now, just return current weights
    return load_current_weights()

def suggest_best_window(recent_n=50):
    """
    Suggest which time window performs best recently
    
    Returns:
        Best performing window name
    """
    leaderboard = get_predictor_leaderboard(recent_n)
    
    window_predictors = {
        'recent_stats': 'Recent 100-300',
        'last_3y': 'Last 3 Years',
        'last_5y': 'Last 5 Years',
        'full_history': 'Full History'
    }
    
    best_predictor = None
    best_score = 0.0
    
    for predictor_name, stats in leaderboard.items():
        if predictor_name in window_predictors:
            score = stats['avg_match_score']
            if score > best_score:
                best_score = score
                best_predictor = predictor_name
    
    if best_predictor:
        return window_predictors[best_predictor]
    else:
        return "Last 5 Years (default)"

def auto_tune_system(recent_n=20):
    """
    Automatically tune the entire system based on recent performance
    
    This is called after new evaluations are added
    """
    print("\n=== Auto-Tuning System ===")
    
    # Update weights
    new_weights = update_weights_after_result(recent_n)
    
    # Suggest best window
    best_window = suggest_best_window(recent_n)
    print(f"\nBest performing window: {best_window}")
    
    # Get leaderboard
    leaderboard = get_predictor_leaderboard(recent_n)
    
    print("\nPredictor Performance (Recent {}):".format(recent_n))
    for predictor_name, stats in leaderboard.items():
        print(f"  {predictor_name}: {stats['avg_match_score']:.2f} avg score, "
              f"{stats['exact_hits']} exact hits")
    
    print("\n=== Auto-Tuning Complete ===\n")
    
    return {
        'weights': new_weights,
        'best_window': best_window,
        'leaderboard': leaderboard
    }
