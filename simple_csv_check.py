import pandas as pd
import re

# Load CSV
df = pd.read_csv('4d_results_history.csv', index_col=False, on_bad_lines='skip')
print(f"CSV loaded: {len(df)} rows, {len(df.columns)} columns")
print(f"Columns: {list(df.columns)}")

# Check first row
print("\nFirst row:")
print(df.iloc[0].to_dict())

# Test number extraction
sample_row = df.iloc[0]
prize_text = str(sample_row.get('prize_text', ''))
if not prize_text or prize_text == 'nan':
    prize_text = str(sample_row.get('3rd', ''))

print(f"\nPrize text sample: {prize_text[:200]}")

# Extract numbers
first_match = re.search(r'1st\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
second_match = re.search(r'2nd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
third_match = re.search(r'3rd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)

print(f"1st Prize: {first_match.group(1) if first_match else 'Not found'}")
print(f"2nd Prize: {second_match.group(1) if second_match else 'Not found'}")
print(f"3rd Prize: {third_match.group(1) if third_match else 'Not found'}")

# Check all 4D numbers in text
all_4d = re.findall(r'\b\d{4}\b', prize_text)
print(f"All 4D numbers found: {all_4d}")