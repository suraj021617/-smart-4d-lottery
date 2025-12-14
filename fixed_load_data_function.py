
def load_data():
    """
    Load and clean lottery data with proper date parsing
    """
    try:
        # Load the CSV file
        df = pd.read_csv('4d_results_history.csv')
        
        # Clean the data - remove rows where date is not actually a date
        df = df[df['date'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)]
        
        # Convert date column properly
        df['Date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
        
        # Remove rows with invalid dates
        df = df[df['Date'].notna()]
        
        # Sort by date to ensure latest data is at the end
        df = df.sort_values('Date')
        
        # Create a proper Numbers column from the available data
        # The winning numbers are actually in the '2nd' column based on CSV structure
        def extract_numbers(row):
            """Extract winning numbers from the row data"""
            import re
            
            # Try to extract from different columns
            text_to_search = str(row.get('2nd', '')) + ' ' + str(row.get('3rd', ''))
            
            # Look for number patterns
            numbers = re.findall(r'\b\d{3,6}\b', text_to_search)
            
            if numbers:
                return numbers[0]  # Return the first number found
            else:
                return ''
        
        df['Numbers'] = df.apply(extract_numbers, axis=1)
        
        # Remove rows without valid numbers
        df = df[df['Numbers'] != '']
        
        # Create Provider column from provider data
        df['Provider'] = df['provider'].apply(lambda x: str(x).split('/')[-1] if '/' in str(x) else str(x))
        
        print(f"Loaded {len(df)} valid lottery entries")
        print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        # Return empty DataFrame with required columns
        return pd.DataFrame(columns=['Date', 'Provider', 'Numbers'])

# Alternative function to load data by lottery type
def load_data_by_type(lottery_type='4D'):
    """
    Load data filtered by lottery type
    """
    df = load_data()
    
    if lottery_type == '4D':
        # Filter for 4-digit numbers
        df = df[df['Numbers'].str.len() == 4]
    elif lottery_type == '5D':
        # Filter for 5-digit numbers
        df = df[df['Numbers'].str.len() == 5]
    elif lottery_type == '6D':
        # Filter for 6-digit numbers
        df = df[df['Numbers'].str.len() == 6]
    
    return df

# Function to check data completeness
def check_data_completeness():
    """Check if data is complete up to target date"""
    try:
        df = load_data()
        if len(df) == 0:
            return False, "No data loaded"
        
        latest_date = df['Date'].max()
        target_date = pd.Timestamp('2025-07-16')
        
        if latest_date < target_date:
            missing_days = (target_date - latest_date).days
            return False, f"Missing {missing_days} days of data (latest: {latest_date.strftime('%Y-%m-%d')})"
        else:
            return True, f"Data is complete (latest: {latest_date.strftime('%Y-%m-%d')})"
            
    except Exception as e:
        return False, f"Error checking data: {e}"
