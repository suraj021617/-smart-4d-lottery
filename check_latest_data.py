import pandas as pd
import re
from datetime import datetime

# Load CSV
df = pd.read_csv('4d_results_history.csv')
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Check latest dates
df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
print(f"\nDate range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")

# Show last 10 rows
print("\n=== LAST 10 ROWS ===")
for i, row in df.tail(10).iterrows():
    print(f"Row {i}: Date={row['date']}, Provider={row['provider']}")
    prize_text = str(row.get('3rd', ''))
    print(f"  Prize text: {prize_text[:100]}...")
    
    # Extract numbers by length
    all_numbers = re.findall(r'\b\d+\b', prize_text)
    numbers_by_length = {}
    for num in all_numbers:
        length = len(num)
        if length not in numbers_by_length:
            numbers_by_length[length] = []
        numbers_by_length[length].append(num)
    
    print(f"  Numbers by length: {numbers_by_length}")
    print("---")

# Check providers and their number formats
print("\n=== PROVIDER ANALYSIS ===")
providers = df['provider'].unique()
for provider in providers:
    if pd.isna(provider):
        continue
    provider_df = df[df['provider'] == provider].tail(5)
    print(f"\nProvider: {provider}")
    
    for _, row in provider_df.iterrows():
        prize_text = str(row.get('3rd', ''))
        numbers = re.findall(r'\b\d{3,6}\b', prize_text)
        if numbers:
            lengths = [len(n) for n in numbers]
            print(f"  Date {row['date']}: Numbers {numbers[:5]} (lengths: {set(lengths)})")