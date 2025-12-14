import pandas as pd
from datetime import datetime
import re

def check_data_issues():
    print("=== CHECKING DATA ISSUES ===")
    
    # Read CSV
    try:
        df = pd.read_csv('4d_results_history.csv')
        print(f"✓ CSV loaded successfully: {len(df)} rows")
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return
    
    # Check date range
    print(f"\n=== DATE RANGE ===")
    print(f"First date: {df['date'].iloc[0]}")
    print(f"Last date: {df['date'].iloc[-1]}")
    
    # Check latest 10 entries
    print(f"\n=== LATEST 10 ENTRIES ===")
    latest_10 = df.tail(10)
    for idx, row in latest_10.iterrows():
        print(f"{row['date']} | {row['provider']} | 1st: {row['1st']} | 2nd: {row['2nd']} | 3rd: {row['3rd']}")
    
    # Check number formats
    print(f"\n=== NUMBER FORMAT ANALYSIS ===")
    
    # Extract numbers from 1st, 2nd, 3rd columns
    all_numbers = []
    for col in ['1st', '2nd', '3rd']:
        for val in df[col].dropna():
            # Extract numbers using regex
            numbers = re.findall(r'\b\d{3,6}\b', str(val))
            all_numbers.extend(numbers)
    
    # Analyze number lengths
    number_lengths = {}
    for num in all_numbers:
        length = len(num)
        if length not in number_lengths:
            number_lengths[length] = 0
        number_lengths[length] += 1
    
    print("Number length distribution:")
    for length, count in sorted(number_lengths.items()):
        print(f"  {length}D numbers: {count}")
    
    # Check providers
    print(f"\n=== PROVIDER ANALYSIS ===")
    providers = df['provider'].value_counts()
    for provider, count in providers.items():
        print(f"  {provider}: {count} entries")
    
    # Check for mixed formats in same entry
    print(f"\n=== MIXED FORMAT DETECTION ===")
    mixed_format_count = 0
    
    for idx, row in df.iterrows():
        numbers_in_row = []
        for col in ['1st', '2nd', '3rd']:
            if pd.notna(row[col]):
                numbers = re.findall(r'\b\d{3,6}\b', str(row[col]))
                numbers_in_row.extend([len(n) for n in numbers])
        
        if len(set(numbers_in_row)) > 1:  # Mixed lengths
            mixed_format_count += 1
            if mixed_format_count <= 5:  # Show first 5 examples
                print(f"  Row {idx}: {row['date']} | {row['provider']} | Lengths: {set(numbers_in_row)}")
    
    print(f"Total mixed format entries: {mixed_format_count}")
    
    # Check for 2025 data specifically
    print(f"\n=== 2025 DATA CHECK ===")
    df_2025 = df[df['date'].str.contains('2025', na=False)]
    print(f"2025 entries: {len(df_2025)}")
    
    if len(df_2025) > 0:
        print("Latest 2025 entries:")
        for idx, row in df_2025.tail(5).iterrows():
            print(f"  {row['date']} | {row['provider']} | 1st: {row['1st']}")

if __name__ == "__main__":
    check_data_issues()