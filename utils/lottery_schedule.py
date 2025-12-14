"""
Malaysian 4D Lottery Schedule Logic
"""
from datetime import datetime, timedelta

# Malaysian 4D lottery schedule (typical)
LOTTERY_DAYS = {
    1: False,  # Monday - No draw
    2: True,   # Tuesday - Some providers
    3: True,   # Wednesday - Main draw day
    4: False,  # Thursday - No draw
    5: False,  # Friday - No draw
    6: True,   # Saturday - Main draw day
    0: True    # Sunday - Main draw day
}

PROVIDER_SCHEDULES = {
    'magnum': [2, 6, 0],      # Tuesday, Saturday, Sunday
    'toto': [1, 3, 6, 0],     # Monday, Wednesday, Saturday, Sunday
    'damacai': [2, 6, 0],     # Tuesday, Saturday, Sunday
    'gdlotto': [2, 6, 0],     # Tuesday, Saturday, Sunday
    'sportstoto': [1, 3, 6, 0] # Monday, Wednesday, Saturday, Sunday
}

def get_next_draw_date(provider='all'):
    """Get the next lottery draw date for a provider"""
    today = datetime.now()
    
    if provider == 'all':
        # Use general schedule
        schedule = [day for day, has_draw in LOTTERY_DAYS.items() if has_draw]
    else:
        schedule = PROVIDER_SCHEDULES.get(provider.lower(), [2, 6, 0])
    
    # Find next draw day
    for i in range(1, 8):  # Check next 7 days
        next_date = today + timedelta(days=i)
        if next_date.weekday() in schedule:
            return next_date
    
    return today + timedelta(days=3)  # Fallback

def get_days_since_last_draw(df, provider='all'):
    """Calculate days since last actual draw"""
    if df.empty:
        return 0
    
    last_draw_date = df['date_parsed'].max()
    today = datetime.now()
    
    return (today - last_draw_date).days

def is_draw_day(date, provider='all'):
    """Check if given date is a draw day"""
    weekday = date.weekday()
    
    if provider == 'all':
        return LOTTERY_DAYS.get(weekday, False)
    else:
        schedule = PROVIDER_SCHEDULES.get(provider.lower(), [2, 6, 0])
        return weekday in schedule

def get_draw_frequency_per_week(provider='all'):
    """Get how many draws per week for a provider"""
    if provider == 'all':
        return sum(1 for has_draw in LOTTERY_DAYS.values() if has_draw)
    else:
        return len(PROVIDER_SCHEDULES.get(provider.lower(), [2, 6, 0]))