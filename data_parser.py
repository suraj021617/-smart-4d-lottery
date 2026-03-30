"""
Data Parser Module - Supports BOTH old and new CSV formats
Safe switching between formats with config flag
"""
import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

def load_old_csv(file_path='4d_results_history.csv'):
    """
    OLD CSV PARSER - Current working format
    """
    try:
        df = pd.read_csv(file_path, index_col=False, on_bad_lines='skip')
        
        # Parse date
        for col in ['date', 'Date', df.columns[0]]:
            if col in df.columns:
                df['date_parsed'] = pd.to_datetime(df[col], errors='coerce')
                break
        
        df.dropna(subset=['date_parsed'], inplace=True)
        
        # Ensure columns exist
        for col in ['1st', '2nd', '3rd', 'special', 'consolation', 'provider']:
            if col not in df.columns:
                df[col] = ''
            else:
                df[col] = df[col].fillna('')
        
        # Normalize provider
        prov_series = df['provider'].astype(str)
        extracted = prov_series.str.extract(r'images/([^,/\s]+)', expand=False)
        df['provider'] = extracted.fillna(prov_series).str.strip().str.lower()
        
        # Extract prizes
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
        
        logger.info(f"✅ Loaded OLD CSV: {len(df)} rows")
        return df
        
    except Exception as e:
        logger.error(f"❌ Error loading old CSV: {e}")
        return pd.DataFrame()

def load_normalized_csv(file_path='4d_results_normalized.csv'):
    """
    NEW NORMALIZED CSV PARSER - Clean format
    """
    try:
        df = pd.read_csv(file_path, index_col=False)
        
        # Parse date
        df['date_parsed'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['date_parsed'], inplace=True)
        
        # Map normalized columns to old format for compatibility
        df['provider'] = df['Provider'].str.lower()
        df['1st_real'] = df['Prize1']
        df['2nd_real'] = df['Prize2']
        df['3rd_real'] = df['Prize3']
        df['special'] = df['SpecialNumbers']
        df['consolation'] = df['ConsolationNumbers']
        df['draw_info'] = df['DrawID']
        
        # Keep original columns too
        df['1st'] = df['Prize1']
        df['2nd'] = df['Prize2']
        df['3rd'] = df['Prize3']
        
        df = df.sort_values(['date_parsed', 'provider']).reset_index(drop=True)
        
        logger.info(f"✅ Loaded NORMALIZED CSV: {len(df)} rows")
        return df
        
    except Exception as e:
        logger.error(f"❌ Error loading normalized CSV: {e}")
        return pd.DataFrame()

def load_csv_smart(use_normalized=False):
    """
    SMART LOADER - Automatically picks the right format
    
    Args:
        use_normalized (bool): If True, use normalized CSV. If False, use old CSV.
    
    Returns:
        DataFrame with consistent column structure
    """
    if use_normalized:
        logger.info("📊 Using NORMALIZED CSV format")
        df = load_normalized_csv()
        if df.empty:
            logger.warning("⚠️ Normalized CSV failed, falling back to old format")
            df = load_old_csv()
    else:
        logger.info("📊 Using OLD CSV format")
        df = load_old_csv()
    
    return df

# Export functions
__all__ = ['load_old_csv', 'load_normalized_csv', 'load_csv_smart']
