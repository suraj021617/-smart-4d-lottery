from flask import Flask, render_template_string
import pandas as pd
import re
from collections import Counter

app = Flask(__name__)

def load_data():
    df = pd.read_csv('4d_results_history.csv')
    df['date_parsed'] = pd.to_datetime(df.iloc[:, 3], errors='coerce')
    df['1st_real'] = df.iloc[:, 4].str.extract(r'1st Prize.*?(\d{4})', expand=False)
    df['2nd_real'] = df.iloc[:, 4].str.extract(r'2nd Prize.*?(\d{4})', expand=False)
    df['3rd_real'] = df.iloc[:, 4].str.extract(r'3rd Prize.*?(\d{4})', expand=False)
    return df.dropna(subset=['date_parsed'])

@app.route('/')
def home():
    df = load_data()
    numbers = []
    for col in ['1st_real', '2nd_real', '3rd_real']:
        numbers.extend([n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()])
    
    freq = Counter(numbers)
    hot = freq.most_common(5)
    cold = freq.most_common()[-5:] if len(freq) >= 5 else []
    
    html = '''
    <h1>🎯 4D Prediction System</h1>
    <div style="display:flex;gap:20px;font-family:Arial">
        <div style="border:1px solid #ddd;padding:15px;border-radius:5px">
            <h3>🔥 Hot Numbers</h3>
            {% for num, count in hot %}
            <div style="font-size:20px;color:red;margin:5px">{{ num }} ({{ count }}x)</div>
            {% endfor %}
        </div>
        <div style="border:1px solid #ddd;padding:15px;border-radius:5px">
            <h3>❄️ Cold Numbers</h3>
            {% for num, count in cold %}
            <div style="font-size:20px;color:blue;margin:5px">{{ num }} ({{ count }}x)</div>
            {% endfor %}
        </div>
    </div>
    <p>Total Draws: {{ total }} | Latest: {{ latest }}</p>
    '''
    
    return render_template_string(html, 
                                hot=hot, 
                                cold=cold, 
                                total=len(df),
                                latest=df['date_parsed'].max().strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)