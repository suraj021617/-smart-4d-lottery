"""
Active Data Filter Module
Creates filtered datasets for different time windows
"""
import pandas as pd
from datetime import datetime, timedelta

def get_recent_n_draws(df, target_date, n=100):
    """
    Get most recent N draws before target date
    
    Args:
        df: Full history dataframe
        target_date: Target prediction date
        n: Number of recent draws
    
    Returns:
        Filtered dataframe with N most recent draws
    """
    from .history_loader import get_data_until_date
    
    past_data = get_data_until_date(df, target_date, exclude_target=True)
    
    # Get unique draw dates
    unique_dates = past_data['date'].unique()
    unique_dates = sorted(unique_dates, reverse=True)
    
    # Take last N dates
    if len(unique_dates) > n:
        cutoff_date = unique_dates[n-1]
        filtered = past_data[past_data['date'] >= cutoff_date]
    else:
        filtered = past_data
    
    return filtered.copy()

def get_recent_100_data(df, target_date):
    """Get recent 100 draws before target date"""
    return get_recent_n_draws(df, target_date, n=100)

def get_recent_300_data(df, target_date):
    """Get recent 300 draws before target date"""
    return get_recent_n_draws(df, target_date, n=300)

def get_last_n_years(df, target_date, years=3):
    """
    Get data from last N years before target date
    
    Args:
        df: Full history dataframe
        target_date: Target prediction date
        years: Number of years to look back
    
    Returns:
        Filtered dataframe with last N years of data
    """
    from .history_loader import get_data_until_date
    
    target_dt = pd.to_datetime(target_date)
    cutoff_date = target_dt - timedelta(days=years*365)
    
    past_data = get_data_until_date(df, target_date, exclude_target=True)
    filtered = past_data[past_data['date'] >= cutoff_date]
    
    return filtered.copy()

def get_last_3y_data(df, target_date):
    """Get last 3 years of data before target date"""
    return get_last_n_years(df, target_date, years=3)

def get_last_5y_data(df, target_date):
    """
    Get last 5 years of data before target date
    This is the DEFAULT ACTIVE LEARNING DATASET
    """
    return get_last_n_years(df, target_date, years=5)

def get_active_5y_data(df, target_date):
    """
    Alias for get_last_5y_data
    This is the main default AI/ML training dataset
    """
    return get_last_5y_data(df, target_date)

def get_full_history_data(df, target_date):
    """
    Get full history before target date
    Use only for reference/analysis, not heavy ML training
    """
    from .history_loader import get_data_until_date
    return get_data_until_date(df, target_date, exclude_target=True)

def get_data_summary(df):
    """Get summary statistics of filtered data"""
    if len(df) == 0:
        return {
            'total_records': 0,
            'date_range': 'No data',
            'unique_numbers': 0,
            'providers': []
        }
    
    return {
        'total_records': len(df),
        'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
        'unique_numbers': df['number'].nunique(),
        'providers': df['provider'].unique().tolist()
    }
