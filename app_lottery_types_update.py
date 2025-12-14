
# Add this to your app.py after the existing imports
import re

def get_lottery_type_from_data(df):
    """Determine what lottery types are available in the data"""
    lottery_types = set()
    
    for _, row in df.iterrows():
        # Check the Numbers column for different formats
        numbers_text = str(row.get('Numbers', ''))
        
        # Look for 4D numbers (4 digits)
        if re.search(r'\b\d{4}\b', numbers_text):
            lottery_types.add('4D')
        
        # Look for 5D numbers (5 digits)  
        if re.search(r'\b\d{5}\b', numbers_text):
            lottery_types.add('5D')
            
        # Look for 6D numbers (6 digits)
        if re.search(r'\b\d{6}\b', numbers_text):
            lottery_types.add('6D')
    
    return list(lottery_types)

def filter_data_by_lottery_type(df, lottery_type):
    """Filter data to only include specific lottery type"""
    if lottery_type == '4D':
        # Filter for 4D numbers only
        return df[df['Numbers'].str.contains(r'\b\d{4}\b', regex=True, na=False)]
    elif lottery_type == '5D':
        # Filter for 5D numbers only  
        return df[df['Numbers'].str.contains(r'\b\d{5}\b', regex=True, na=False)]
    elif lottery_type == '6D':
        # Filter for 6D numbers only
        return df[df['Numbers'].str.contains(r'\b\d{6}\b', regex=True, na=False)]
    else:
        return df

# Add this route to your app.py
@app.route('/lottery-types')
def lottery_types():
    """Show different lottery type options"""
    try:
        df = load_data()
        available_types = get_lottery_type_from_data(df)
        
        return render_template('lottery_types.html', 
                             lottery_types=available_types)
    except Exception as e:
        return f"Error: {e}"

# Update your existing prediction routes to accept lottery type
@app.route('/best-predictions/<lottery_type>')
def best_predictions_by_type(lottery_type='4D'):
    """Generate predictions for specific lottery type"""
    try:
        df = load_data()
        
        # Filter data by lottery type
        filtered_df = filter_data_by_lottery_type(df, lottery_type)
        
        if len(filtered_df) == 0:
            return f"No {lottery_type} data available"
        
        # Your existing prediction logic here, but use filtered_df
        # ... rest of your prediction code ...
        
        return render_template('best_predictions.html',
                             predictions=predictions,
                             lottery_type=lottery_type,
                             next_draw_date=next_draw_date,
                             next_draw_day=next_draw_day)
    except Exception as e:
        return f"Error generating {lottery_type} predictions: {e}"
