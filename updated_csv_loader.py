"""
Updated CSV Loader for app.py
Replace the load_csv_data() function with this
"""
import threading
from datetime import datetime
import pandas as pd
import logging

# Import the new modules
try:
    from data_parser import load_csv_smart
    from csv_config import USE_NORMALIZED_DATA
    USE_NEW_SYSTEM = True
except ImportError:
    USE_NEW_SYSTEM = False
    logging.warning("⚠️ New CSV system not available, using old loader")

logger = logging.getLogger(__name__)

# Cache variables
_csv_cache = None
_csv_cache_time = None
_csv_lock = threading.Lock()

def load_csv_data():
    """
    UPDATED CSV LOADER with safe switching
    
    Controlled by csv_config.py:
    - USE_NORMALIZED_DATA = False → Uses old CSV (default, safe)
    - USE_NORMALIZED_DATA = True → Uses new normalized CSV (after testing)
    """
    global _csv_cache, _csv_cache_time
    
    with _csv_lock:
        # Check cache
        if _csv_cache is not None and _csv_cache_time is not None:
            if (datetime.now() - _csv_cache_time).total_seconds() < 300:
                return _csv_cache.copy()
    
    try:
        if USE_NEW_SYSTEM:
            # Use new smart loader with config switch
            df = load_csv_smart(use_normalized=USE_NORMALIZED_DATA)
            
            if USE_NORMALIZED_DATA:
                logger.info("✅ Using NORMALIZED CSV format")
            else:
                logger.info("✅ Using OLD CSV format (safe mode)")
        else:
            # Fallback to old loader
            logger.info("✅ Using OLD CSV loader (fallback)")
            df = _load_old_csv_fallback()
        
        if df.empty:
            logger.warning("⚠️ CSV is empty")
            return df
        
        # Update cache
        _csv_cache = df.copy()
        _csv_cache_time = datetime.now()
        
        return df
        
    except Exception as e:
        logger.error(f"❌ CSV loading error: {e}")
        return pd.DataFrame()

def _load_old_csv_fallback():
    """Fallback to original old CSV loader"""
    import warnings
    warnings.filterwarnings('ignore', category=pd.errors.ParserWarning)
    
    df = pd.read_csv('4d_results_history.csv', index_col=False, on_bad_lines='skip')
    
    for col in ['date', 'Date']:
        if col in df.columns:
            df['date_parsed'] = pd.to_datetime(df[col], errors='coerce')
            break
    
    df.dropna(subset=['date_parsed'], inplace=True)
    
    for col in ['1st', '2nd', '3rd', 'special', 'consolation', 'provider']:
        if col not in df.columns:
            df[col] = ''
        else:
            df[col] = df[col].fillna('')
    
    import re
    prov_series = df['provider'].astype(str)
    extracted = prov_series.str.extract(r'images/([^,/\s]+)', expand=False)
    df['provider'] = extracted.fillna(prov_series).str.strip().str.lower()
    
    def extract_prize_numbers(row):
        prize_text = str(row.get('3rd', ''))
        first_match = re.search(r'1st[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        second_match = re.search(r'2nd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        third_match = re.search(r'3rd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        
        return pd.Series({
            '1st_real': first_match.group(1) if first_match else '',
            '2nd_real': second_match.group(1) if second_match else '',
            '3rd_real': third_match.group(1) if third_match else ''
        })
    
    df[['1st_real', '2nd_real', '3rd_real']] = df.apply(extract_prize_numbers, axis=1)
    df = df.sort_values(['date_parsed', 'provider']).reset_index(drop=True)
    
    return df
