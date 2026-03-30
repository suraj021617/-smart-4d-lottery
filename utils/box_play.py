"""Box Play Suggestions - Generate all permutations"""
from itertools import permutations

def generate_box_play(number):
    """Generate all unique permutations of a 4D number"""
    if not number or len(str(number)) != 4:
        return []
    
    num_str = str(number).zfill(4)
    
    # Generate all permutations
    perms = set([''.join(p) for p in permutations(num_str)])
    
    return sorted(list(perms))

def generate_ibox(number):
    """Generate iBox (unique digits only)"""
    num_str = str(number).zfill(4)
    unique_digits = len(set(num_str))
    
    if unique_digits == 4:
        # All different digits - 24 permutations
        return generate_box_play(number), 24
    elif unique_digits == 3:
        # One pair - 12 permutations
        perms = generate_box_play(number)
        return perms, 12
    elif unique_digits == 2:
        # Two pairs or triple - 6 or 4 permutations
        perms = generate_box_play(number)
        return perms, len(perms)
    else:
        # All same - 1 permutation
        return [num_str], 1

def calculate_box_cost(number, bet_amount=1):
    """Calculate cost for box play"""
    perms, count = generate_ibox(number)
    return {
        'number': number,
        'permutations': perms,
        'total_combinations': count,
        'cost_per_bet': bet_amount,
        'total_cost': bet_amount * count
    }

def suggest_box_plays(predictions):
    """Suggest box plays for multiple predictions"""
    suggestions = []
    for pred in predictions:
        if isinstance(pred, tuple):
            num = pred[0]
        else:
            num = pred
        
        box_info = calculate_box_cost(num)
        suggestions.append(box_info)
    
    return suggestions
