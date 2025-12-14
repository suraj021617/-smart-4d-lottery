"""
Fix for the data parsing issue in app.py
This will help your system read data up to 2025-07-16
"""

def create_fixed_load_data_function():
    """Create a fixed version of the load_data function"""
    
    fixed_code = '''
def load_data():
    """
    Load and clean lottery data with proper date parsing
    """
    try:
        # Load the CSV file
        df = pd.read_csv('4d_results_history.csv')
        
        # Clean the data - remove rows where date is not actually a date
        df = df[df['date'].str.match(r'\\d{4}-\\d{2}-\\d{2}', na=False)]
        
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
            numbers = re.findall(r'\\b\\d{3,6}\\b', text_to_search)
            
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
'''

    with open('fixed_load_data_function.py', 'w', encoding='utf-8') as f:
        f.write(fixed_code)
    
    print("[OK] Created fixed_load_data_function.py")

def create_app_integration_guide():
    """Create guide for integrating the fixes"""
    
    guide = '''
=== APP.PY INTEGRATION GUIDE ===

STEP 1: REPLACE YOUR load_data() FUNCTION
Replace your existing load_data() function in app.py with the code from 'fixed_load_data_function.py'

STEP 2: ADD LOTTERY TYPE ROUTES
Add these routes to your app.py:

@app.route('/lottery-types')
def lottery_types():
    """Show lottery type selection page"""
    return render_template('lottery_types.html', 
                         lottery_types=['4D', '5D', '6D'])

@app.route('/best-predictions/<lottery_type>')
def best_predictions_by_type(lottery_type='4D'):
    """Generate predictions for specific lottery type"""
    try:
        # Use the new load_data_by_type function
        df = load_data_by_type(lottery_type)
        
        if len(df) == 0:
            return f"No {lottery_type} data available"
        
        # Your existing prediction logic here
        predictions = generate_predictions(df)  # Your existing function
        
        return render_template('best_predictions.html',
                             predictions=predictions,
                             lottery_type=lottery_type,
                             provider='all',
                             next_draw_date=get_next_draw_date(),
                             next_draw_day=get_next_draw_day())
    except Exception as e:
        return f"Error: {e}"

STEP 3: UPDATE YOUR HOME PAGE
Add this button to your main page template:

<a href="/lottery-types" class="nav-btn">🎲 Select Lottery Type</a>

STEP 4: ADD DATA CHECK ROUTE (OPTIONAL)
Add this route to check data completeness:

@app.route('/data-status')
def data_status():
    """Check data completeness"""
    is_complete, message = check_data_completeness()
    return f"Data Status: {message}"

STEP 5: TEST THE FIXES
1. Start your app
2. Go to /data-status to check if data loads properly
3. Go to /lottery-types to see the lottery selection
4. Click on "4D Lottery" to test 4D predictions
5. Click on "5D Lottery" to test 5D predictions
6. Click on "6D Lottery" to test 6D predictions

TROUBLESHOOTING:
- If you get "No data available", check your CSV file path
- If dates are wrong, the load_data() function will filter them out
- If predictions are still mixed, make sure you're using load_data_by_type()

This should fix:
✓ Mixed number formats (4D, 5D, 6D separated)
✓ Data parsing issues (proper date filtering)
✓ Wrong predictions (type-specific predictions)
'''

    with open('APP_INTEGRATION_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("[OK] Created APP_INTEGRATION_GUIDE.txt")

if __name__ == "__main__":
    print("=== CREATING DATA PARSING FIXES ===")
    
    create_fixed_load_data_function()
    create_app_integration_guide()
    
    print("\n[SUCCESS] DATA PARSING FIXES CREATED!")
    print("\nFiles created:")
    print("1. fixed_load_data_function.py - Fixed data loading code")
    print("2. APP_INTEGRATION_GUIDE.txt - Step-by-step integration guide")
    
    print("\nThis will fix:")
    print("✓ Data parsing stops at 2025-07-13")
    print("✓ Mixed number formats (4D, 5D, 6D)")
    print("✓ Wrong prediction dates")
    print("✓ System prediction failures")
    
    print("\nNext: Follow the APP_INTEGRATION_GUIDE.txt to update your app.py")