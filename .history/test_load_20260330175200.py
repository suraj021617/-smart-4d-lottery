import sys
sys.path.append('.')

from app import load_csv_data

print("Testing load_csv_data...")
df = load_csv_data()
print(f"Loaded {len(df)} rows")
print(f"Columns: {list(df.columns)}")
print(f"Sample row:\n{df.head(1).T}")