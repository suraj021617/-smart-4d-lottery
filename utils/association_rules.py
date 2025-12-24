"""
Association Rules Mining (Apriori Algorithm)
Finds "If X appears, then Y likely appears" patterns
"""
from collections import defaultdict, Counter
from itertools import combinations

def association_rules_predictor(df, min_support=0.05, min_confidence=0.3):
    """
    Association Rules Mining
    Finds number combinations that frequently appear together
    """
    try:
        # Extract numbers by draw
        draws = []
        for _, row in df.iterrows():
            draw_numbers = []
            for col in ['number_1st', 'number_2nd', 'number_3rd']:
                if col in row and row[col] and len(str(row[col])) == 4:
                    draw_numbers.append(str(row[col]))
            if draw_numbers:
                draws.append(set(draw_numbers))
        
        if len(draws) < 10:
            return []
        
        # Use recent draws
        recent_draws = draws[-100:]
        total_draws = len(recent_draws)
        
        # Find frequent itemsets (numbers that appear together)
        itemset_counts = Counter()
        
        # Single items
        for draw in recent_draws:
            for num in draw:
                itemset_counts[frozenset([num])] += 1
        
        # Pairs
        for draw in recent_draws:
            for pair in combinations(draw, 2):
                itemset_counts[frozenset(pair)] += 1
        
        # Filter by minimum support
        min_count = int(total_draws * min_support)
        frequent_itemsets = {k: v for k, v in itemset_counts.items() if v >= min_count}
        
        # Generate association rules
        rules = []
        for itemset, count in frequent_itemsets.items():
            if len(itemset) == 2:
                items = list(itemset)
                # Rule: if items[0] then items[1]
                antecedent_count = itemset_counts.get(frozenset([items[0]]), 0)
                if antecedent_count > 0:
                    confidence = count / antecedent_count
                    if confidence >= min_confidence:
                        support = count / total_draws
                        lift = confidence / (itemset_counts.get(frozenset([items[1]]), 0) / total_draws)
                        rules.append({
                            'if': items[0],
                            'then': items[1],
                            'confidence': confidence,
                            'support': support,
                            'lift': lift
                        })
        
        # Get last drawn number
        last_draw = recent_draws[-1] if recent_draws else set()
        
        # Find predictions based on rules
        predictions = {}
        for rule in rules:
            if rule['if'] in last_draw:
                score = rule['confidence'] * rule['lift']
                predictions[rule['then']] = max(predictions.get(rule['then'], 0), score)
        
        # Sort and return top 5
        sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return [(num, score, f'Association-rule') for num, score in sorted_predictions[:5]]
    
    except Exception as e:
        return []


def find_frequent_patterns(df, min_support=3):
    """
    Find frequently occurring number patterns
    """
    try:
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            if col in df.columns:
                all_numbers.extend([n for n in df[col].dropna() if n and len(str(n)) == 4])
        
        if len(all_numbers) < 10:
            return []
        
        # Find digit patterns
        pattern_counts = Counter()
        
        for num in all_numbers[-100:]:
            digits = [int(d) for d in num]
            
            # Pattern types
            if len(set(digits)) == 1:
                pattern_counts['AAAA'] += 1
            elif len(set(digits)) == 2:
                if digits.count(digits[0]) == 2:
                    pattern_counts['AABB'] += 1
                else:
                    pattern_counts['AAAB'] += 1
            elif len(set(digits)) == 3:
                pattern_counts['AABC'] += 1
            else:
                pattern_counts['ABCD'] += 1
        
        # Return most common patterns
        return pattern_counts.most_common(3)
    
    except Exception as e:
        return []
