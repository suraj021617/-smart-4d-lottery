"""
Quick fix script to add safe date handling throughout app.py
This adds a helper function to safely handle date operations
"""

# Add this helper function at the top of app.py after imports:

HELPER_FUNCTION = """
# ============ SAFE DATE HELPER ============
def safe_date_max(series):
    '''Safely get max date, handling NaT values'''
    if series.empty:
        return datetime.now()
    max_date = series.max()
    if pd.notna(max_date):
        return max_date
    return datetime.now()

def safe_strftime(date_value, format_str='%Y-%m-%d'):
    '''Safely format date, handling NaT values'''
    if pd.notna(date_value):
        return date_value.strftime(format_str)
    return datetime.now().strftime(format_str)
# ==========================================
"""

print("Add this helper function after the imports in app.py:")
print(HELPER_FUNCTION)
print("\nThen replace all instances of:")
print("  df['date_parsed'].max().strftime(...)")
print("With:")
print("  safe_strftime(safe_date_max(df['date_parsed']), ...)")
