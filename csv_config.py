"""
Configuration File - Control CSV format switching
"""

# ============================================
# 🔧 CSV FORMAT CONTROL
# ============================================

# Set to False = Use OLD CSV (current working system)
# Set to True = Use NEW NORMALIZED CSV (after testing)
USE_NORMALIZED_DATA = False

# ============================================
# 📁 FILE PATHS
# ============================================

OLD_CSV_PATH = '4d_results_history.csv'
NORMALIZED_CSV_PATH = '4d_results_normalized.csv'

# ============================================
# 🔐 SECURITY
# ============================================

SECRET_KEY = 'your-secret-key-here'

# ============================================
# 📊 DATA SETTINGS
# ============================================

# Cache timeout in seconds (5 minutes)
CACHE_TIMEOUT = 300

# Maximum rows to process for predictions
MAX_PREDICTION_ROWS = 500

# ============================================
# 🎯 PREDICTION SETTINGS
# ============================================

# Default lookback periods
ADVANCED_LOOKBACK = 200
SMART_LOOKBACK = 300
ML_LOOKBACK = 500

# ============================================
# 📝 LOGGING
# ============================================

LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
