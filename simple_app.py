from flask import Flask, render_template, request
import pandas as pd
import re
from collections import Counter
from utils.predictor import frequency_predictor, hot_cold_analysis, extract_4d_numbers
from utils.learning_engine import analyze_predictions_vs_results, calculate_learning_stats

app = Flask(__name__)

def load_data():
    """Load and process CSV data"""
    try:
        df = pd.read_csv('4d_results_history.csv')
        # Parse dates
        df['date_parsed'] = pd.to_datetime(df.iloc[:, 3], errors='coerce')
        # Extract prize text
        df['1st_real'] = df.iloc[:, 4].str.extract(r'1st Prize.*?(\d{4})', expand=False)
        df['2nd_real'] = df.iloc[:, 4].str.extract(r'2nd Prize.*?(\d{4})', expand=False)
        df['3rd_real'] = df.iloc[:, 4].str.extract(r'3rd Prize.*?(\d{4})', expand=False)
        return df.dropna(subset=['date_parsed'])
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

@app.route('/')
def home():
    df = load_data()
    if df.empty:
        return "No data available"
    
    # Get basic stats
    total_draws = len(df)
    latest_date = df['date_parsed'].max().strftime('%Y-%m-%d') if not df.empty else 'N/A'
    
    # Get predictions
    predictions = frequency_predictor(df, 5)
    hot_cold = hot_cold_analysis(df, 30)
    
    return render_template('index.html', 
                         total_draws=total_draws,
                         latest_date=latest_date,
                         predictions=predictions,
                         hot_numbers=hot_cold['hot'][:5],
                         cold_numbers=hot_cold['cold'][:5])

@app.route('/predictions')
def predictions():
    df = load_data()
    provider = request.args.get('provider', 'all')
    
    if provider != 'all':
        df = df[df.iloc[:, 1].str.contains(provider, case=False, na=False)]
    
    predictions = frequency_predictor(df, 10)
    return render_template('predictions.html', predictions=predictions, provider=provider)

@app.route('/statistics')
def statistics():
    df = load_data()
    numbers = extract_4d_numbers(df)
    
    freq = Counter(numbers)
    digit_freq = Counter(''.join(numbers))
    
    return render_template('statistics.html', 
                         number_freq=freq.most_common(20),
                         digit_freq=digit_freq.most_common(10))

@app.route('/daily-learning-system')
def daily_learning_system():
    df = load_data()
    provider = request.args.get('provider', 'all')
    
    # Filter by provider
    if provider != 'all':
        df = df[df.iloc[:, 1].str.contains(provider, case=False, na=False)]
    
    # Get learning data
    learning_data = analyze_predictions_vs_results(df)
    learning_stats = calculate_learning_stats(learning_data)
    
    provider_options = ['all', 'magnum', 'damacai', 'toto', 'stc4d']
    
    return render_template('daily_learning_system.html',
                         learning_data=learning_data,
                         learning_stats=learning_stats,
                         provider_options=provider_options,
                         provider=provider)

if __name__ == '__main__':
    app.run(debug=True, port=5001)