import pandas as pd

df = pd.read_csv('4d_results_history.csv', nrows=3)
print('Columns:', df.columns.tolist())
print('\nFirst row:')
for col in df.columns:
    print(f'{col}: {df[col].iloc[0]}')
