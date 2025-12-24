"""
Pure Markov Chain Predictor - Uses ONLY CSV data transitions
No fake predictions - only real numbers that actually followed in history
"""
from collections import defaultdict, Counter

def build_markov_chain(historical_draws):
    """
    Build transition matrix from historical 1st Prize numbers
    Shows: What number followed each number in history
    """
    if not historical_draws or len(historical_draws) < 2:
        return {}
    
    transitions = defaultdict(lambda: defaultdict(int))
    
    for i in range(len(historical_draws) - 1):
        current = str(historical_draws[i])
        next_num = str(historical_draws[i + 1])
        
        if len(current) == 4 and len(next_num) == 4 and current.isdigit() and next_num.isdigit():
            transitions[current][next_num] += 1
    
    return transitions

def predict_from_markov(today_number, transitions, all_historical):
    """
    For today's 1st Prize, show what actually followed it in history
    Returns: Real numbers with confidence scores
    """
    predictions = []
    today_str = str(today_number)
    
    if len(today_str) != 4 or not today_str.isdigit():
        return []
    
    # Direct lookup: What followed this number before?
    if today_str in transitions:
        next_candidates = transitions[today_str]
        total_occurrences = sum(next_candidates.values())
        
        for next_num, count in sorted(next_candidates.items(), key=lambda x: x[1], reverse=True):
            confidence = (count / total_occurrences) * 100
            predictions.append((next_num, confidence, f"Followed {count}x"))
    
    # Fallback: If today's number never appeared, use most frequent numbers
    if not predictions and all_historical:
        freq = Counter(all_historical)
        for num, count in freq.most_common(10):
            confidence = (count / len(all_historical)) * 100
            predictions.append((num, confidence, f"Historical frequency"))
    
    return predictions[:23]  # Return 23 predictions

def get_markov_statistics(transitions):
    """
    Get statistics about the Markov chain
    """
    stats = {
        'unique_numbers': len(transitions),
        'total_transitions': sum(sum(v.values()) for v in transitions.values()),
        'avg_transitions_per_number': 0,
        'most_connected': None,
        'least_connected': None
    }
    
    if transitions:
        transition_counts = [len(v) for v in transitions.values()]
        stats['avg_transitions_per_number'] = sum(transition_counts) / len(transition_counts)
        
        # Most connected (has most different followers)
        most_connected_num = max(transitions.items(), key=lambda x: len(x[1]))
        stats['most_connected'] = {
            'number': most_connected_num[0],
            'followers': len(most_connected_num[1])
        }
        
        # Least connected
        least_connected_num = min(transitions.items(), key=lambda x: len(x[1]))
        stats['least_connected'] = {
            'number': least_connected_num[0],
            'followers': len(least_connected_num[1])
        }
    
    return stats
