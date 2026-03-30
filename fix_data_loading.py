# QUICK FIX FOR DATA LOADING ISSUE
# Add this to app.py to replace the load_csv_data function

def load_csv_data():
    """
    Load CSV with SIMPLE parsing - no complex normalization
    """
    global _csv_cache, _csv_last_modified
    
    try:
        import warnings
        warnings.filterwarnings('ignore', category=pd.errors.ParserWarning)
        
        csv_paths = ['4d_results_history.csv', 'utils/4d_results_history.csv']
        df = None
        csv_path = None
        
        for path in csv_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if not csv_path:
            logger.error("No CSV file found")
            return pd.DataFrame()
        
        # Check if file was modified
        current_mtime = os.path.getmtime(csv_path)
        if _csv_cache is not None and current_mtime == _csv_last_modified:
            logger.info(f"Using cached data ({len(_csv_cache)} rows)")
            return _csv_cache.copy()
        
        # Load fresh data - SIMPLE PARSING
        df = pd.read_csv(csv_path, index_col=False, on_bad_lines='skip')
        if not df.empty:
            df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
            logger.info(f"FRESH LOAD from: {csv_path} ({len(df)} rows) - File modified!")
            _csv_last_modified = current_mtime
        
        if df is None or df.empty:
            logger.error("No valid CSV file found")
            return pd.DataFrame()
            
    except Exception as e:
        logger.error(f"CSV loading error: {e}")
        return pd.DataFrame()

    # SIMPLE NORMALIZATION - NO COMPLEX FILTERING
    # Parse date
    df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
    
    # Normalize provider
    df['provider_key'] = df['provider'].astype(str).str.lower().str.strip()
    
    # Map provider names
    provider_map = {
        'toto': 'Sports Toto',
        'damacai': 'Da Ma Cai',
        'magnum': 'Magnum 4D',
        'gdlotto': 'GD Lotto',
        'sabah88': 'Sabah 88',
        'sandakan': 'Sandakan',
        'cashsweep': 'Cash Sweep',
        'singapore': 'Singapore'
    }
    
    for key, name in provider_map.items():
        df.loc[df['provider_key'].str.contains(key, na=False), 'provider_key'] = name
    
    # Extract numbers from columns
    df['number_1st'] = df['1st'].astype(str).str.extract(r'(\d{4})', expand=False)
    df['number_2nd'] = df['2nd'].astype(str).str.extract(r'(\d{4})', expand=False)
    df['number_3rd'] = df['3rd'].astype(str).str.extract(r'(\d{4})', expand=False)
    
    # Keep special and consolation as-is
    df['special'] = df['special'].fillna('')
    df['consolation'] = df['consolation'].fillna('')
    
    # Filter: must have date and at least one number
    df = df[
        df['date_parsed'].notna() & 
        (df['number_1st'].notna() | df['number_2nd'].notna() | df['number_3rd'].notna())
    ].copy()
    
    # Sort by date descending (newest first)
    df = df.sort_values('date_parsed', ascending=False).reset_index(drop=True)
    
    # ADD ALIASES for backward compatibility
    df['1st_real'] = df['number_1st']
    df['2nd_real'] = df['number_2nd']
    df['3rd_real'] = df['number_3rd']
    df['provider'] = df['provider_key']
    
    # Cache the result
    _csv_cache = df.copy()
    
    logger.info(f"Data ready: {len(df)} rows | Latest: {df['date_parsed'].max()}")
    
    return df
