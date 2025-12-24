import pandas as pd

df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')

print(f"Total columns: {len(df.columns)}")
print(f"Column names: {df.columns.tolist()}")
print(f"\nFirst row:")
for i, col in enumerate(df.columns):
    print(f"  Col {i}: {col} = {df.iloc[0, i]}")

print(f"\nLooking for 1st Prize in row 0:")
for i, val in enumerate(df.iloc[0]):
    if '1st Prize' in str(val):
        print(f"  Found at column {i}: {val}")
