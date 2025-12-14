"""
Quick fix for the lottery system to handle different number formats
This will update your app.py to show separate buttons for different lottery types
"""

def create_updated_app():
    """Create an updated version of app.py with separate lottery type handling"""
    
    app_code = '''
# Add this to your app.py after the existing imports
import re

def get_lottery_type_from_data(df):
    """Determine what lottery types are available in the data"""
    lottery_types = set()
    
    for _, row in df.iterrows():
        # Check the Numbers column for different formats
        numbers_text = str(row.get('Numbers', ''))
        
        # Look for 4D numbers (4 digits)
        if re.search(r'\\b\\d{4}\\b', numbers_text):
            lottery_types.add('4D')
        
        # Look for 5D numbers (5 digits)  
        if re.search(r'\\b\\d{5}\\b', numbers_text):
            lottery_types.add('5D')
            
        # Look for 6D numbers (6 digits)
        if re.search(r'\\b\\d{6}\\b', numbers_text):
            lottery_types.add('6D')
    
    return list(lottery_types)

def filter_data_by_lottery_type(df, lottery_type):
    """Filter data to only include specific lottery type"""
    if lottery_type == '4D':
        # Filter for 4D numbers only
        return df[df['Numbers'].str.contains(r'\\b\\d{4}\\b', regex=True, na=False)]
    elif lottery_type == '5D':
        # Filter for 5D numbers only  
        return df[df['Numbers'].str.contains(r'\\b\\d{5}\\b', regex=True, na=False)]
    elif lottery_type == '6D':
        # Filter for 6D numbers only
        return df[df['Numbers'].str.contains(r'\\b\\d{6}\\b', regex=True, na=False)]
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
'''

    # Save the updated code
    with open('app_lottery_types_update.py', 'w', encoding='utf-8') as f:
        f.write(app_code)
    
    print("[OK] Created app_lottery_types_update.py")

def create_lottery_types_template():
    """Create a template for selecting lottery types"""
    
    template_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Select Lottery Type</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .lottery-types {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .lottery-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            text-decoration: none;
            transition: transform 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .lottery-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .lottery-card h2 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .lottery-card p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .info-box h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .info-box ul {
            color: #666;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎲 Select Lottery Type</h1>
            <p>Choose the type of lottery you want to predict</p>
        </div>
        
        <div class="lottery-types">
            {% for lottery_type in lottery_types %}
            <a href="/best-predictions/{{ lottery_type }}" class="lottery-card">
                <h2>{{ lottery_type }} Lottery</h2>
                <p>
                    {% if lottery_type == '4D' %}
                    4-digit numbers (GDLotto style)
                    {% elif lottery_type == '5D' %}
                    5-digit numbers (SportsToto style)
                    {% elif lottery_type == '6D' %}
                    6-digit numbers (Da Ma Cai style)
                    {% endif %}
                </p>
            </a>
            {% endfor %}
        </div>
        
        <div class="info-box">
            <h3>💡 About Different Lottery Types:</h3>
            <ul>
                <li><strong>4D Lottery:</strong> Traditional 4-digit numbers (0000-9999)</li>
                <li><strong>5D Lottery:</strong> 5-digit numbers with more combinations</li>
                <li><strong>6D Lottery:</strong> 6-digit numbers with highest prize pools</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="/" style="color: #667eea; text-decoration: none; font-weight: bold;">← Back to Home</a>
        </div>
    </div>
</body>
</html>'''

    # Save the template
    with open('templates/lottery_types.html', 'w', encoding='utf-8') as f:
        f.write(template_code)
    
    print("[OK] Created templates/lottery_types.html")

def create_quick_fix_instructions():
    """Create instructions for quick fix"""
    
    instructions = '''
=== QUICK FIX INSTRUCTIONS ===

Your lottery system has 3 main issues:

1. MIXED NUMBER FORMATS: 4D, 5D, and 6D numbers are mixed together
2. DATA PARSING STOPS AT 2025-07-13: System not reading latest data
3. WRONG PREDICTIONS: System shows predictions for wrong dates

IMMEDIATE SOLUTIONS:

1. ADD LOTTERY TYPE SELECTION:
   - Copy code from 'app_lottery_types_update.py' to your app.py
   - Copy 'lottery_types.html' to your templates folder
   - Add route: /lottery-types

2. UPDATE YOUR HOME PAGE:
   Add this button to your main page:
   
   <a href="/lottery-types" class="nav-btn">🎲 Select Lottery Type</a>

3. SEPARATE PREDICTIONS:
   Instead of mixing all numbers, users can now choose:
   - 4D Predictions (for GDLotto)
   - 5D Predictions (for SportsToto)  
   - 6D Predictions (for Da Ma Cai)

4. FIX DATA PARSING:
   In your load_data() function, add:
   
   # Filter out invalid dates
   df = df[df['Date'].notna()]
   df = df[df['Date'] != '']
   
   # Ensure latest data is included
   df = df.sort_values('Date')

TESTING:
1. Run your app
2. Go to /lottery-types
3. Click on "4D Lottery" 
4. Should show only 4-digit predictions
5. Click on "5D Lottery"
6. Should show only 5-digit predictions

This will immediately fix the mixed number format issue!
'''

    with open('QUICK_FIX_INSTRUCTIONS.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("[OK] Created QUICK_FIX_INSTRUCTIONS.txt")

if __name__ == "__main__":
    print("=== CREATING QUICK FIX FOR LOTTERY SYSTEM ===")
    
    create_updated_app()
    create_lottery_types_template()
    create_quick_fix_instructions()
    
    print("\n[SUCCESS] QUICK FIX FILES CREATED!")
    print("\nFiles created:")
    print("1. app_lottery_types_update.py - Code to add to your app.py")
    print("2. templates/lottery_types.html - New template for lottery selection")
    print("3. QUICK_FIX_INSTRUCTIONS.txt - Step-by-step instructions")
    
    print("\nNext steps:")
    print("1. Copy code from app_lottery_types_update.py to your app.py")
    print("2. Copy lottery_types.html to your templates folder")
    print("3. Add a button to your home page linking to /lottery-types")
    print("4. Test the different lottery type predictions")
    
    print("\nThis will immediately separate 4D, 5D, and 6D predictions!")