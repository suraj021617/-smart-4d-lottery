"""
REST API endpoints for Smart 4D System
Provides JSON API for mobile apps and external integrations
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Get predictions via API"""
    try:
        from app import load_csv_data, advanced_predictor, smart_auto_weight_predictor, ml_predictor
        
        provider = request.args.get('provider', 'all')
        method = request.args.get('method', 'advanced')
        limit = int(request.args.get('limit', 5))
        
        df = load_csv_data()
        
        if method == 'advanced':
            predictions = advanced_predictor(df, provider, 200)[:limit]
        elif method == 'smart':
            predictions = smart_auto_weight_predictor(df, provider, 300)[:limit]
        elif method == 'ml':
            predictions = ml_predictor(df, 500)[:limit]
        else:
            predictions = advanced_predictor(df, provider, 200)[:limit]
        
        result = [{
            'number': num,
            'confidence': float(score),
            'method': reason
        } for num, score, reason in predictions]
        
        return jsonify({
            'success': True,
            'data': result,
            'provider': provider,
            'method': method,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/results/latest', methods=['GET'])
def get_latest_results():
    """Get latest lottery results"""
    try:
        from app import load_csv_data
        
        df = load_csv_data()
        provider = request.args.get('provider', 'all')
        limit = int(request.args.get('limit', 10))
        
        if provider != 'all':
            df = df[df['provider_key'] == provider]
        
        results = []
        for _, row in df.head(limit).iterrows():
            results.append({
                'date': row['date_parsed'].strftime('%Y-%m-%d'),
                'provider': row['provider_key'],
                'first': row.get('number_1st', ''),
                'second': row.get('number_2nd', ''),
                'third': row.get('number_3rd', '')
            })
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"API results error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get lottery statistics"""
    try:
        from app import load_csv_data
        from collections import Counter
        
        df = load_csv_data()
        provider = request.args.get('provider', 'all')
        
        if provider != 'all':
            df = df[df['provider_key'] == provider]
        
        all_numbers = []
        for col in ['number_1st', 'number_2nd', 'number_3rd']:
            all_numbers.extend([n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()])
        
        freq = Counter(all_numbers)
        hot_numbers = [{'number': num, 'count': count} for num, count in freq.most_common(10)]
        cold_numbers = [{'number': num, 'count': count} for num, count in freq.most_common()[-10:]]
        
        return jsonify({
            'success': True,
            'data': {
                'total_draws': len(df),
                'hot_numbers': hot_numbers,
                'cold_numbers': cold_numbers,
                'unique_numbers': len(freq)
            },
            'provider': provider,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"API statistics error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/providers', methods=['GET'])
def get_providers():
    """Get list of available providers"""
    try:
        from app import load_csv_data
        
        df = load_csv_data()
        providers = sorted([p for p in df['provider_key'].dropna().unique() if p])
        
        return jsonify({
            'success': True,
            'data': providers,
            'count': len(providers),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"API providers error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
