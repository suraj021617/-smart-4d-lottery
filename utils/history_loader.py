"""
History Loader Module
Loads full CSV history with caching, deduplication, and file change detection
"""
import pandas as pd
import os
from datetime import datetime
import hashlib

# Global cache
_history_cache = None
_cache_file_hash = None

def get_file_hash(filepath):
    """Get file modification hash for cache invalidation"""
    stat = os.stat(filepath)
    return f"{stat.st_mtime}_{stat.st_size}"

def load_history_data(csv_path='4d_results_history.csv', force_reload=False):
    """
    Load full historical data with intelligent caching
    
    Rules:
    - Load full history from 2015 to 2025
    - Normalize all numbers to 4-digit format
    - Parse dates correctly
    - Drop duplicate rows
    - Cache data but invalidate if file changes
    
    Returns:
        DataFrame with columns: date, provider, number, draw_no, etc.
    """
    global _history_cache, _cache_file_hash
    
    # Check if cache is valid
    current_hash = get_file_hash(csv_path)
    if not force_reload and _history_cache is not None and _cache_file_hash == current_hash:
        print("✓ Using cached history data")
        return _history_cache.copy()
    
    print("⟳ Loading history from CSV...")
    
    # Load CSV
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Parse dates
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    elif df.columns[0].lower() in ['date', 'draw_date']:
        df.rename(columns={df.columns[0]: 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['date'])
    
    # Extract 4D numbers from various columns
    numbers = []
    for idx, row in df.iterrows():
        row_numbers = extract_4d_numbers_from_row(row)
        for num in row_numbers:
            numbers.append({
                'date': row['date'],
                'provider': row.get('provider', 'Unknown'),
                'number': num,
                'draw_no': row.get('draw_no', '')
            })
    
    # Create clean dataframe
    clean_df = pd.DataFrame(numbers)
    
    # Normalize numbers to 4 digits
    clean_df['number'] = clean_df['number'].apply(normalize_to_4d)
    
    # Drop invalid numbers
    clean_df = clean_df[clean_df['number'].notna()]
    
    # Drop duplicates
    clean_df = clean_df.drop_duplicates(subset=['date', 'provider', 'number'])
    
    # Sort by date
    clean_df = clean_df.sort_values('date').reset_index(drop=True)
    
    print(f"✓ Loaded {len(clean_df)} records from {clean_df['date'].min()} to {clean_df['date'].max()}")
    
    # Update cache
    _history_cache = clean_df.copy()
    _cache_file_hash = current_hash
    
    return clean_df.copy()

def extract_4d_numbers_from_row(row):
    """Extract all valid 4D numbers from a row"""
    numbers = []
    
    # Check common column patterns
    for col in row.index:
        val = str(row[col])
        
        # Extract 4D numbers using patterns
        if 'prize' in col.lower() or 'winner' in col.lower() or 'result' in col.lower():
            extracted = extract_4d_from_text(val)
            numbers.extend(extracted)
    
    return numbers

def extract_4d_from_text(text):
    """Extract 4D numbers from text"""
    import re
    numbers = []
    
    # Find all 4-digit sequences
    matches = re.findall(r'\b(\d{4})\b', text)
    for match in matches:
        numbers.append(match)
    
    return numbers

def normalize_to_4d(number):
    """Normalize number to 4-digit format"""
    try:
        num_str = str(number).strip()
        # Remove non-digits
        num_str = ''.join(filter(str.isdigit, num_str))
        
        if len(num_str) == 0:
            return None
        
        # Convert to int and back to remove leading zeros, then pad
        num_int = int(num_str)
        
        # Only accept 0-9999
        if num_int < 0 or num_int > 9999:
            return None
        
        # Format as 4 digits
        return f"{num_int:04d}"
    except:
        return None

def get_data_until_date(df, target_date, exclude_target=True):
    """
    Get data strictly before target date (anti-leakage rule)
    
    Args:
        df: Full history dataframe
        target_date: Target prediction date
        exclude_target: If True, exclude target date (default for prediction)
    
    Returns:
        Filtered dataframe with only past data
    """
    target_dt = pd.to_datetime(target_date)
    
    if exclude_target:
        # Strict: only data BEFORE target date
        return df[df['date'] < target_dt].copy()
    else:
        # Include target date (for evaluation after result is known)
        return df[df['date'] <= target_dt].copy()

def clear_cache():
    """Force clear cache (useful for testing)"""
    global _history_cache, _cache_file_hash
    _history_cache = None
    _cache_file_hash = None
    print("✓ Cache cleared")
