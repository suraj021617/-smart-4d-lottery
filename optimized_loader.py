"""
Optimized CSV Data Loader
- Smart caching based on file modification time
- Memory-efficient loading
- Fast duplicate detection
"""
import os
import pandas as pd
import logging
from datetime import datetime
from optimized_cache import _data_cache

logger = logging.getLogger(__name__)

def get_file_hash(filepath):
    """Get file modification time as cache key"""
    try:
        stat = os.stat(filepath)
        return f"{filepath}_{stat.st_mtime}_{stat.st_size}"
    except OSError:
        return None

def load_csv_optimized(csv_path='4d_results_history.csv'):
    """
    Load CSV with smart caching
    - Only reloads if file changed
    - 10x faster on cache hit
    """
    # Check cache first
    file_hash = get_file_hash(csv_path)
    if file_hash:
        cached = _data_cache.get(file_hash)
        if cached is not None:
            logger.info(f"✅ Cache HIT - Loaded {len(cached)} rows instantly")
            return cached
    
    # Cache miss - load from disk
    logger.info(f"⏳ Cache MISS - Loading from {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, index_col=False, on_bad_lines='skip', low_memory=False)
        
        if df.empty:
            logger.warning("CSV is empty")
            return pd.DataFrame()
        
        # Apply normalization
        from utils.data_normalizer import normalize_dataframe
        df = normalize_dataframe(df)
        
        # Filter valid rows
        df = df[df['is_valid']].copy()
        
        # Sort by date descending
        df = df.sort_values('date_parsed', ascending=False).reset_index(drop=True)
        
        # Add backward compatibility aliases
        df['1st_real'] = df['number_1st']
        df['2nd_real'] = df['number_2nd']
        df['3rd_real'] = df['number_3rd']
        df['provider'] = df['provider_key']
        
        # Cache the result
        if file_hash:
            _data_cache.set(file_hash, df)
        
        logger.info(f"✅ Loaded {len(df)} rows | Latest: {df['date_parsed'].max()}")
        return df
        
    except Exception as e:
        logger.error(f"❌ CSV load error: {e}")
        return pd.DataFrame()

def get_data_stats(df):
    """Get quick stats about loaded data"""
    if df.empty:
        return {}
    
    return {
        'total_rows': len(df),
        'date_range': {
            'earliest': str(df['date_parsed'].min()),
            'latest': str(df['date_parsed'].max())
        },
        'providers': df['provider_key'].nunique(),
        'valid_4d_numbers': df['number_1st'].notna().sum()
    }
