"""
SUPER PREDICTOR - Combines ALL Advanced Methods
LSTM + XGBoost + Markov + Association Rules + Existing Methods
"""
from collections import Counter

def super_predictor(df, advanced_preds, smart_preds, ml_preds):
    """
    Ultimate predictor combining all methods with intelligent weighting
    
    Args:
        df: DataFrame with historical data
        advanced_preds: Predictions from advanced_predictor
        smart_preds: Predictions from smart_auto_weight_predictor
        ml_preds: Predictions from ml_predictor
    
    Returns:
        Top 5 predictions with confidence scores
    """
    try:
        # Import new predictors
        try:
            from utils.lstm_predictor import lstm_predictor
            from utils.xgboost_predictor import xgboost_predictor
            from utils.markov_predictor import markov_chain_predictor, markov_multi_step
            from utils.association_rules import association_rules_predictor
            
            # Get predictions from new methods
            lstm_preds = lstm_predictor(df, lookback=100) or []
            xgb_preds = xgboost_predictor(df, lookback=150) or []
            markov_preds = markov_chain_predictor(df, lookback=200) or []
            markov_multi = markov_multi_step(df, steps=3, lookback=200) or []
            assoc_preds = association_rules_predictor(df) or []
            
        except ImportError:
            lstm_preds = []
            xgb_preds = []
            markov_preds = []
            markov_multi = []
            assoc_preds = []
        
        # Weighted scoring system
        weighted_scores = {}
        
        # Method weights (based on theoretical accuracy)
        weights = {
            'advanced': 1.0,
            'smart': 1.0,
            'ml': 0.9,
            'lstm': 1.3,      # Higher weight for sequence learning
            'xgboost': 1.4,   # Highest weight for ensemble
            'markov': 1.2,    # Good for transitions
            'markov_multi': 1.1,
            'association': 1.0
        }
        
        # Combine all predictions
        all_predictions = [
            (advanced_preds, 'advanced'),
            (smart_preds, 'smart'),
            (ml_preds, 'ml'),
            (lstm_preds, 'lstm'),
            (xgb_preds, 'xgboost'),
            (markov_preds, 'markov'),
            (markov_multi, 'markov_multi'),
            (assoc_preds, 'association')
        ]
        
        # Score each number
        for preds, method in all_predictions:
            weight = weights.get(method, 1.0)
            for num, score, reason in preds[:10]:  # Top 10 from each
                if num not in weighted_scores:
                    weighted_scores[num] = {
                        'score': 0,
                        'votes': 0,
                        'methods': []
                    }
                weighted_scores[num]['score'] += score * weight
                weighted_scores[num]['votes'] += 1
                weighted_scores[num]['methods'].append(method)
        
        # Calculate final scores with consensus bonus
        final_scores = {}
        for num, data in weighted_scores.items():
            # Base score
            base_score = data['score'] / max(data['votes'], 1)
            
            # Consensus bonus (more methods = higher confidence)
            consensus_bonus = data['votes'] * 0.1
            
            # Method diversity bonus
            unique_methods = len(set(data['methods']))
            diversity_bonus = unique_methods * 0.05
            
            # Final score
            final_scores[num] = base_score + consensus_bonus + diversity_bonus
        
        # Sort and return top 5
        sorted_predictions = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for num, score in sorted_predictions[:5]:
            methods_used = '+'.join(set(weighted_scores[num]['methods']))
            confidence = min(int(score * 100), 99)
            results.append({
                'number': num,
                'confidence': confidence,
                'score': round(score, 3),
                'votes': weighted_scores[num]['votes'],
                'methods': methods_used
            })
        
        return results
    
    except Exception as e:
        # Fallback to existing methods
        return []


def get_prediction_insights(super_results):
    """
    Generate insights from super predictor results
    """
    insights = []
    
    if not super_results:
        return ["No predictions available"]
    
    # Confidence analysis
    avg_confidence = sum(r['confidence'] for r in super_results) / len(super_results)
    if avg_confidence > 80:
        insights.append(f"🔥 High confidence predictions (avg {avg_confidence:.0f}%)")
    elif avg_confidence > 60:
        insights.append(f"✅ Good confidence predictions (avg {avg_confidence:.0f}%)")
    else:
        insights.append(f"⚠️ Moderate confidence (avg {avg_confidence:.0f}%)")
    
    # Consensus analysis
    max_votes = max(r['votes'] for r in super_results)
    if max_votes >= 6:
        insights.append(f"💪 Strong consensus ({max_votes}/8 methods agree)")
    elif max_votes >= 4:
        insights.append(f"👍 Good consensus ({max_votes}/8 methods agree)")
    
    # Method diversity
    all_methods = set()
    for r in super_results:
        all_methods.update(r['methods'].split('+'))
    insights.append(f"🎯 Using {len(all_methods)} different AI methods")
    
    return insights
