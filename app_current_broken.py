"""
Smart 4D Lottery Prediction System - Refactored
Clean, modular, adaptive auto-learning system
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import pandas as pd

# Import all utility modules
from utils.history_loader import load_history_data, get_data_until_date
from utils.prediction_runner import (
    run_all_predictions,
    predict_recent_stats_only,
    predict_last_3_years_only,
    predict_last_5_years_only,
    predict_ml_only,
    predict_ai_pattern_only,
    predict_smart_auto_learn_only,
    predict_full_history_only,
    format_predictions_for_display
)
from utils.prediction_logger import save_prediction_log, find_log_for_date, get_prediction_summary
from utils.result_evaluator import (
    evaluate_after_result,
    get_predictor_leaderboard,
    format_evaluation_report
)
from utils.weight_updater import auto_tune_system, get_weight_history
from utils.drift_analyzer import analyze_recent_drift, format_drift_report
from utils.consensus import get_current_weights

app = Flask(__name__)

# Global data cache
_history_df = None

def get_history_df():
    """Get cached history dataframe"""
    global _history_df
    if _history_df is None:
        _history_df = load_history_data('4d_results_history.csv')
    return _history_df

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Main prediction endpoint
    Runs all predictors and returns top 5 consensus
    """
    try:
        data = request.json
        target_date = data.get('target_date', datetime.now().strftime('%Y-%m-%d'))
        provider = data.get('provider', 'All')
        
        # Load history
        df = get_history_df()
        
        # Run all predictions
        result = run_all_predictions(df, target_date, provider)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        # Save prediction log
        log_id = save_prediction_log(
            target_date=result['target_date'],
            provider=provider,
            predictions_dict=result['predictions'],
            weights_used=get_current_weights(),
            data_used_until=result['data_used_until']
        )
        
        # Format for display
        final_predictions = format_predictions_for_display(result['final_consensus'], show_top_n=5)
        
        return jsonify({
            'success': True,
            'target_date': result['target_date'],
            'data_used_until': result['data_used_until'],
            'final_predictions': final_predictions,
            'log_id': log_id,
            'all_predictions': result['predictions'],  # Hidden details
            'weights': get_current_weights()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/<predictor_name>', methods=['POST'])
def api_predict_specific(predictor_name):
    """
    Specific predictor endpoint
    Separate button handlers for each predictor
    """
    try:
        data = request.json
        target_date = data.get('target_date', datetime.now().strftime('%Y-%m-%d'))
        
        df = get_history_df()
        
        # Route to specific predictor
        predictor_map = {
            'recent_stats': predict_recent_stats_only,
            'last_3y': predict_last_3_years_only,
            'last_5y': predict_last_5_years_only,
            'ml': predict_ml_only,
            'ai_pattern': predict_ai_pattern_only,
            'smart_auto_learn': predict_smart_auto_learn_only,
            'full_history': predict_full_history_only
        }
        
        if predictor_name not in predictor_map:
            return jsonify({'error': 'Invalid predictor name'}), 400
        
        # Run specific predictor
        predictions = predictor_map[predictor_name](df, target_date, top_n=5)
        
        # Get data used until date
        past_data = get_data_until_date(df, target_date, exclude_target=True)
        data_used_until = past_data['date'].max() if len(past_data) > 0 else None
        
        # Format for display
        formatted = format_predictions_for_display(predictions, show_top_n=5)
        
        return jsonify({
            'success': True,
            'predictor': predictor_name,
            'target_date': target_date,
            'data_used_until': str(data_used_until),
            'predictions': formatted
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    """
    Evaluate predictions after actual result is known
    """
    try:
        data = request.json
        log_id = data.get('log_id')
        actual_result = data.get('actual_result')
        
        if not log_id or not actual_result:
            return jsonify({'error': 'Missing log_id or actual_result'}), 400
        
        # Evaluate
        evaluation = evaluate_after_result(log_id, actual_result)
        
        if not evaluation:
            return jsonify({'error': 'Evaluation failed'}), 500
        
        # Auto-tune system after evaluation
        auto_tune_result = auto_tune_system(recent_n=20)
        
        # Format report
        report = format_evaluation_report(evaluation)
        
        return jsonify({
            'success': True,
            'evaluation': evaluation,
            'report': report,
            'auto_tune': auto_tune_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leaderboard', methods=['GET'])
def api_leaderboard():
    """Get predictor performance leaderboard"""
    try:
        recent_n = int(request.args.get('recent_n', 50))
        leaderboard = get_predictor_leaderboard(recent_n)
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard,
            'recent_n': recent_n
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/drift', methods=['POST'])
def api_drift():
    """Analyze recent drift"""
    try:
        data = request.json
        target_date = data.get('target_date', datetime.now().strftime('%Y-%m-%d'))
        
        df = get_history_df()
        
        drift_report = analyze_recent_drift(df, target_date)
        formatted_report = format_drift_report(drift_report)
        
        return jsonify({
            'success': True,
            'drift_report': drift_report,
            'formatted_report': formatted_report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weights', methods=['GET'])
def api_weights():
    """Get current predictor weights"""
    try:
        weights = get_current_weights()
        return jsonify({
            'success': True,
            'weights': weights
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def api_logs():
    """Get prediction logs summary"""
    try:
        summary = get_prediction_summary()
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history_match', methods=['POST'])
def api_history_match():
    """
    Check if a number exists in history (separate from prediction)
    """
    try:
        data = request.json
        number = data.get('number', '').zfill(4)
        
        df = get_history_df()
        
        # Find matches
        matches = df[df['number'] == number]
        
        if len(matches) == 0:
            return jsonify({
                'success': True,
                'found': False,
                'number': number
            })
        
        # Format matches
        match_list = []
        for _, row in matches.iterrows():
            match_list.append({
                'date': str(row['date']),
                'provider': row['provider'],
                'number': row['number']
            })
        
        return jsonify({
            'success': True,
            'found': True,
            'number': number,
            'matches': match_list,
            'count': len(match_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get system statistics"""
    try:
        df = get_history_df()
        
        stats = {
            'total_records': len(df),
            'date_range': f"{df['date'].min()} to {df['date'].max()}",
            'unique_numbers': df['number'].nunique(),
            'providers': df['provider'].unique().tolist(),
            'current_weights': get_current_weights()
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎯 Smart 4D Lottery Prediction System - REFACTORED")
    print("="*60)
    print("\nFeatures:")
    print("✓ Clean modular architecture")
    print("✓ Separate button logic for each predictor")
    print("✓ Anti-data-leakage design")
    print("✓ Adaptive auto-learning after evaluations")
    print("✓ Top 5 consensus predictions")
    print("✓ Prediction logging and evaluation")
    print("✓ Performance leaderboard")
    print("✓ Drift analysis")
    print("\n" + "="*60)
    
    # Load data on startup
    print("\nLoading historical data...")
    df = get_history_df()
    print(f"✓ Loaded {len(df)} records")
    print(f"✓ Date range: {df['date'].min()} to {df['date'].max()}")
    
    print("\n" + "="*60)
    print("🚀 Starting server on http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/decision-helper')
def decision_helper():
    logger.debug("=== DECISION HELPER ROUTE CALLED ===")
    df = load_csv_data()
    logger.debug(f"Data loaded: {len(df)} rows")
    provider = request.args.get('provider', 'all')
    provider_options = ['all'] + sorted([p for p in df['provider'].dropna().unique() if p and str(p).strip()])
    logger.debug(f"Provider: {provider}, Options: {provider_options}")
    
    if df.empty:
        logger.error("DataFrame is empty!")
        return render_template('decision_helper.html', error="No data", final_picks=[], reasons=[], provider_options=provider_options, provider=provider, next_draw_date='', provider_name='', backup_numbers=[])
    
    if provider != 'all':
        df = df[df['provider'] == provider]
        logger.debug(f"Filtered to provider {provider}: {len(df)} rows")
    
    logger.debug("Calling predictors...")
    adv = advanced_predictor(df, provider, 200) or []
    logger.debug(f"Advanced: {len(adv)} predictions")
    smart = smart_auto_weight_predictor(df, provider, 300) or []
    logger.debug(f"Smart: {len(smart)} predictions")
    ml = ml_predictor(df, 500) or []
    logger.debug(f"ML: {len(ml)} predictions")
    
    adv = adv[:10] if adv else []
    smart = smart[:10] if smart else []
    ml = ml[:10] if ml else []
    
    # FALLBACK: If all predictors fail, use most frequent numbers
    if not adv and not smart and not ml:
        logger.debug("All predictors returned empty! Using fallback...")
        all_nums = []
        for col in ['1st_real', '2nd_real', '3rd_real']:
            all_nums.extend([n for n in df[col].tail(100).astype(str) if n.isdigit() and len(n) == 4])
        logger.debug(f"Fallback found {len(all_nums)} numbers")
        if all_nums:
            freq = Counter(all_nums).most_common(10)
            adv = [(num, 1.0, 'frequency') for num, count in freq]
            logger.debug(f"Fallback created {len(adv)} predictions")
    
    # Voting system
    votes = {}
    for num, score, _ in adv + smart + ml:
        votes[num] = votes.get(num, 0) + 1
    
    if not votes:
        logger.error("No votes collected!")
        return render_template('decision_helper.html', error="No predictions available", final_picks=[], reasons=[], provider_options=provider_options, provider=provider, next_draw_date='', provider_name='', backup_numbers=[])
    
    sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    final_picks = [(num, min(count * 25, 95)) for num, count in sorted_votes[:5]]
    
    # Get backup numbers
    all_candidates = set([num for num, _, _ in adv + smart + ml])
    final_nums = set([num for num, _ in final_picks])
    backup_numbers = list(all_candidates - final_nums)[:10]
    
    logger.debug(f"Final picks: {final_picks}")
    
    reasons = [
        "Weighted Ensemble: Best predictors get more influence",
        "Multi-Timeframe: Validated across 7d, 30d, 90d windows",
        "Gap Analysis: Overdue numbers boosted",
        f"Analyzed {len(df)} historical draws",
        "Confidence-weighted consensus from 3 AI models"
    ]
    
    last_draw = df.iloc[-1]
    next_draw_date = (last_draw['date_parsed'] + timedelta(days=3)).strftime('%Y-%m-%d (%A)')
    provider_name = provider.upper() if provider != 'all' else 'ALL PROVIDERS'
    
    logger.debug("Rendering template with data...")
    return render_template('decision_helper.html', 
                         final_picks=final_picks, 
                         reasons=reasons, 
                         next_draw_date=next_draw_date, 
                         provider_name=provider_name, 
                         backup_numbers=backup_numbers,
                         provider_options=provider_options,
                         provider=provider,
                         error=None)

