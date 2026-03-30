"""
Provider Filtering Helper
Add this to app.py to fix provider filtering issues
"""

def filter_by_provider(df, provider_param):
    """
    Standardized provider filtering logic
    
    Args:
        df: DataFrame with 'provider_key' column
        provider_param: Provider string from request.args.get('provider')
    
    Returns:
        Filtered DataFrame
    """
    if not provider_param or provider_param == 'all':
        return df
    
    # Normalize the provider parameter
    from utils.data_normalizer import DataNormalizer
    normalized_provider = DataNormalizer.normalize_provider(provider_param)
    
    # Filter using normalized provider key
    filtered = df[df['provider_key'] == normalized_provider]
    
    # If no results, try case-insensitive partial match as fallback
    if filtered.empty:
        provider_lower = provider_param.lower().strip()
        mask = df['provider_key'].str.lower().str.contains(provider_lower, na=False)
        filtered = df[mask]
    
    return filtered


# USAGE EXAMPLE:
# Replace this pattern:
#   if provider != 'all':
#       df = df[df['provider_key'] == provider]
#
# With this:
#   df = filter_by_provider(df, provider)
