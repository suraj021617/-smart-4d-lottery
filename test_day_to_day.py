"""
Test day-to-day prediction logic
"""
import pandas as pd
from utils.data_normalizer import normalize_dataframe
from utils.day_to_day_learner import learn_day_to_day_patterns, predict_tomorrow
import re

# Load CSV
df = pd.read_csv('4d_results_history.csv', index_col=False, on_bad_lines='skip')
df = normalize_dataframe(df)
df = df[df['is_valid']].copy()
df = df.sort_values('date_parsed', ascending=True).tail(100)

print(f"Loaded {len(df)} rows")

# Get latest date
latest_date = df['date_parsed'].max()
today_data = df[df['date_parsed'] == latest_date]

print(f"\nLatest date: {latest_date.strftime('%Y-%m-%d')}")
print(f"Rows for latest date: {len(today_data)}")

# Extract today's numbers (including Special + Consolation)
today_numbers = []
for _, row in today_data.iterrows():
    # 1st, 2nd, 3rd
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        num = str(row.get(col, ''))
        if len(num) == 4 and num.isdigit():
            today_numbers.append(num)
    
    # Special
    special_str = str(row.get('special', '')).strip()
    if special_str and special_str not in ['nan', '', 'None']:
        special_nums = re.findall(r'\b\d{4}\b', special_str)
        today_numbers.extend([n for n in special_nums if n != '----' and n != '****'])
    
    # Consolation
    consolation_str = str(row.get('consolation', '')).strip()
    if consolation_str and consolation_str not in ['nan', '', 'None']:
        consolation_nums = re.findall(r'\b\d{4}\b', consolation_str)
        today_numbers.extend([n for n in consolation_nums if n != '----' and n != '****'])

# Remove duplicates
seen = set()
today_numbers = [n for n in today_numbers if not (n in seen or seen.add(n))]

print(f"\nToday's numbers extracted: {len(today_numbers)}")
print(f"First 10: {today_numbers[:10]}")

# Build historical draws
historical_draws = []
for _, row in df.iterrows():
    for col in ['number_1st', 'number_2nd', 'number_3rd']:
        num = str(row.get(col, ''))
        if len(num) == 4 and num.isdigit():
            historical_draws.append({'number': num, 'date': row['date_parsed']})

print(f"\nHistorical draws: {len(historical_draws)}")

# Learn patterns
patterns = learn_day_to_day_patterns(historical_draws)
print(f"\nPatterns learned:")
print(f"  - Digit transitions: {len(patterns.get('digit_transitions', {}))} digits")
print(f"  - Sequence patterns: {len(patterns.get('sequence_patterns', {}))} sequences")

# Get recent numbers
recent_nums = [draw['number'] for draw in historical_draws[-20:]]

# Generate predictions
predictions = predict_tomorrow(today_numbers, patterns, recent_nums)

print(f"\nPredictions generated: {len(predictions)}")
for i, (num, score, reason) in enumerate(predictions[:5], 1):
    print(f"  {i}. {num} (score: {score:.2f}) - {reason}")

if not predictions:
    print("\nNO PREDICTIONS GENERATED!")
    print("Debugging:")
    print(f"  - today_numbers: {len(today_numbers)}")
    print(f"  - patterns: {bool(patterns)}")
    print(f"  - recent_nums: {len(recent_nums)}")
