"""
Integration module for Smart 4D enhancements
Add this to your app.py to enable new features

Usage:
    from app_enhancements import enhance_app
    enhance_app(app)
"""
import logging

logger = logging.getLogger(__name__)

def enhance_app(app):
    """
    Enhance existing Flask app with new features
    WITHOUT removing any existing functionality
    """
    
    # 1. Register API Blueprint
    try:
        from api_routes import api_bp
        app.register_blueprint(api_bp)
        logger.info("✅ API routes registered at /api/v1")
    except Exception as e:
        logger.warning(f"API routes not registered: {e}")
    
    # 2. Initialize WebSocket (optional)
    try:
        from websocket_handler import init_socketio
        socketio = init_socketio(app)
        if socketio:
            logger.info("✅ WebSocket support enabled")
            return socketio
    except Exception as e:
        logger.warning(f"WebSocket not initialized: {e}")
    
    # 3. Initialize Database (optional)
    try:
        from database import Database
        db = Database()
        db.import_from_csv('4d_results_history.csv')
        logger.info("✅ Database layer initialized")
    except Exception as e:
        logger.warning(f"Database not initialized: {e}")
    
    # 4. Add caching to existing routes
    try:
        from cache_system import cache_result, prediction_cache
        app.config['PREDICTION_CACHE'] = prediction_cache
        logger.info("✅ Caching system enabled")
    except Exception as e:
        logger.warning(f"Caching not enabled: {e}")
    
    logger.info("🚀 App enhancements completed!")
    return None

def add_performance_monitoring(app):
    """Add performance monitoring (optional)"""
    @app.before_request
    def before_request():
        from flask import g
        import time
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        from flask import g, request
        import time
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            if elapsed > 1.0:  # Log slow requests
                logger.warning(f"Slow request: {request.path} took {elapsed:.2f}s")
        return response
    
    logger.info("✅ Performance monitoring enabled")

def add_error_handling(app):
    """Add enhanced error handling"""
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify, request
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Not found'}), 404
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify, request
        logger.error(f"Internal error: {error}")
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return "Internal server error", 500
    
    logger.info("✅ Error handling enhanced")
