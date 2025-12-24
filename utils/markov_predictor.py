"""
Markov Chain Predictor
Predicts next state based on current state transitions
"""
from collections import defaultdict, Counter

def markov_chain_predictor(df, lookback=200):
    """
    Markov Chain predictor
    Learns transition probabilities between numbers
    """
    try:
        # Extract numbers
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            if col in df.columns:
                all_numbers.extend([n for n in df[col].dropna() if n and len(str(n)) == 4])
        
        if len(all_numbers) < 10:
            return []
        
        recent = all_numbers[-lookback:]
        
        # Build transition matrix
        transitions = defaultdict(lambda: Counter())
        
        for i in range(len(recent) - 1):
            current_state = recent[i]
            next_state = recent[i + 1]
            transitions[current_state][next_state] += 1
        
        # Get current state (last drawn number)
        current = recent[-1] if recent else None
        
        if not current or current not in transitions:
            # Fallback: use most common transitions
            all_transitions = Counter()
            for state_transitions in transitions.values():
                all_transitions.update(state_transitions)
            
            predictions = []
            for num, count in all_transitions.most_common(5):
                prob = count / sum(all_transitions.values())
                predictions.append((num, prob, 'Markov-fallback'))
            return predictions
        
        # Calculate transition probabilities from current state
        next_states = transitions[current]
        total = sum(next_states.values())
        
        predictions = []
        for num, count in next_states.most_common(5):
            probability = count / total
            predictions.append((num, probability, f'Markov-from-{current}'))
        
        return predictions
    
    except Exception as e:
        return []


def markov_multi_step(df, steps=3, lookback=200):
    """
    Multi-step Markov Chain
    Predicts multiple steps ahead
    """
    try:
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            if col in df.columns:
                all_numbers.extend([n for n in df[col].dropna() if n and len(str(n)) == 4])
        
        if len(all_numbers) < 10:
            return []
        
        recent = all_numbers[-lookback:]
        
        # Build multi-step transitions
        transitions = defaultdict(lambda: Counter())
        
        for i in range(len(recent) - steps):
            state_sequence = tuple(recent[i:i+steps])
            next_state = recent[i + steps]
            transitions[state_sequence][next_state] += 1
        
        # Get current state sequence
        current_sequence = tuple(recent[-steps:]) if len(recent) >= steps else None
        
        if not current_sequence or current_sequence not in transitions:
            return markov_chain_predictor(df, lookback)
        
        # Predict from current sequence
        next_states = transitions[current_sequence]
        total = sum(next_states.values())
        
        predictions = []
        for num, count in next_states.most_common(5):
            probability = count / total
            predictions.append((num, probability, f'Markov-{steps}step'))
        
        return predictions
    
    except Exception as e:
        return []
