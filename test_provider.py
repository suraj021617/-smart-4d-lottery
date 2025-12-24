import pandas as pd
import re

# Read CSV
df = pd.read_csv('4d_results_history.csv', nrows=20, on_bad_lines='skip')

print("=== CHECKING PROVIDER DATA ===\n")
print(f"Total rows: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}\n")

# Check provider column
print("Provider column samples:")
for i, val in enumerate(df['provider'].head(10)):
    print(f"{i}: '{val}'")

# Check if provider info is in the '3rd' column (prize text)
print("\n\n=== CHECKING '3rd' COLUMN FOR PROVIDER INFO ===")
for i in range(min(3, len(df))):
    prize_text = str(df.iloc[i]['3rd'])
    print(f"\nRow {i} prize text (first 200 chars):")
    print(prize_text[:200])
    
    # Try to find provider name
    if 'toto' in prize_text.lower():
        print("  -> Contains 'toto'")
    if 'magnum' in prize_text.lower():
        print("  -> Contains 'magnum'")
    if 'damacai' in prize_text.lower() or 'da ma cai' in prize_text.lower():
        print("  -> Contains 'damacai'")
