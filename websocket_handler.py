"""
WebSocket support for real-time updates
Allows live prediction updates without page refresh
"""
from flask_socketio import SocketIO, emit
import logging

logger = logging.getLogger(__name__)

socketio = None

def init_socketio(app):
    """Initialize SocketIO with Flask app"""
    global socketio
    try:
        socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
        logger.info("SocketIO initialized successfully")
        
        @socketio.on('connect')
        def handle_connect():
            logger.info("Client connected")
            emit('connection_response', {'status': 'connected'})
        
        @socketio.on('disconnect')
        def handle_disconnect():
            logger.info("Client disconnected")
        
        @socketio.on('request_predictions')
        def handle_prediction_request(data):
            """Handle real-time prediction requests"""
            try:
                from app import load_csv_data, advanced_predictor
                
                provider = data.get('provider', 'all')
                df = load_csv_data()
                predictions = advanced_predictor(df, provider, 200)[:5]
                
                result = [{
                    'number': num,
                    'confidence': float(score),
                    'method': reason
                } for num, score, reason in predictions]
                
                emit('predictions_update', {'predictions': result, 'provider': provider})
            except Exception as e:
                logger.error(f"WebSocket prediction error: {e}")
                emit('error', {'message': str(e)})
        
        return socketio
    except ImportError:
        logger.warning("flask-socketio not installed. WebSocket features disabled.")
        return None

def broadcast_new_result(result_data):
    """Broadcast new lottery result to all connected clients"""
    if socketio:
        socketio.emit('new_result', result_data, broadcast=True)

def broadcast_prediction_update(predictions):
    """Broadcast prediction update to all connected clients"""
    if socketio:
        socketio.emit('prediction_update', predictions, broadcast=True)
