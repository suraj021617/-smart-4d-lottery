import pandas as pd

print("FIXING CSV PARSING ERROR...")

# Read with error handling
df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip', engine='python')

print(f"Loaded {len(df)} rows successfully")
print(f"Columns: {list(df.columns)}")

# Save cleaned version
df.to_csv('4d_results_history.csv', index=False)
print("CSV FIXED! Restart your Flask app now.")
