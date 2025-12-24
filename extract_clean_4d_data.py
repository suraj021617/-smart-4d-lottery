import csv
import re
import pandas as pd
from datetime import datetime

input_file = '4d_results_history.csv'
output_file = 'clean_4d_training_data.csv'

def is_valid_4d(num):
    """Validate 4D number: exactly 4 digits, 0000-9999"""
    return num and len(num) == 4 and num.isdigit() and 0 <= int(num) <= 9999

def extract_4d_numbers(text):
    """Extract only valid 4D numbers from text"""
    numbers = re.findall(r'\b\d{4}\b', text)
    return [n for n in numbers if is_valid_4d(n)]

pattern = re.compile(r'1st.*?(\d{4})\D+2nd.*?(\d{4})\D+3rd.*?(\d{4})')
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})')

results = []

with open(input_file, encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            line = str(row)
            match = pattern.search(line)
            
            if match:
                first, second, third = match.group(1), match.group(2), match.group(3)
                
                if is_valid_4d(first) and is_valid_4d(second) and is_valid_4d(third):
                    date_str = row.get('date', '') or row.get('draw_date', '')
                    provider = row.get('provider', 'Unknown')
                    
                    results.append({
                        'date': date_str,
                        'provider': provider,
                        '1st': first,
                        '2nd': second,
                        '3rd': third
                    })
        except Exception as e:
            continue

df = pd.DataFrame(results)
df = df.drop_duplicates(subset=['date', 'provider', '1st', '2nd', '3rd'])
df = df.sort_values('date', ascending=False)
df.to_csv(output_file, index=False)
print(f"✅ Extracted {len(df)} clean 4D rows to '{output_file}'")
print(f"📊 Providers: {df['provider'].nunique()} | Date range: {df['date'].min()} to {df['date'].max()}")
