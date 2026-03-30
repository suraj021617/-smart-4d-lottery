import pandas as pd
from utils.data_normalizer import normalize_dataframe

# Load and normalize data
df = pd.read_csv('4d_results_history.csv', index_col=False, on_bad_lines='skip')
df = normalize_dataframe(df)
df = df[df['is_valid']].copy()
df = df.sort_values('date_parsed', ascending=False).reset_index(drop=True)

print("=== TESTING FILTERS ===\n")

# Test provider options
print("PROVIDER OPTIONS:")
provider_options = ['all']
for p in df['provider_key'].dropna().unique():
    p_str = str(p).strip()
    if p_str and p_str.lower() != 'nan' and len(p_str) >= 2:
        provider_options.append(p_str)
provider_options = sorted(list(set(provider_options)))
for p in provider_options:
    print(f"  - {p}")

print("\n" + "="*50 + "\n")

# Test month options
print("MONTH OPTIONS:")
month_options = sorted(df['date_parsed'].dropna().dt.strftime('%Y-%m').unique(), reverse=True)
for m in month_options:
    print(f"  - {m}")

print("\n" + "="*50 + "\n")

# Test default month
default_month = df['date_parsed'].max().strftime('%Y-%m')
print(f"DEFAULT MONTH: {default_month}")

print("\n" + "="*50 + "\n")

# Test filtering
test_month = '2025-12'
test_provider = 'gdlotto'

filtered = df[df['date_parsed'].dt.strftime('%Y-%m') == test_month]
print(f"Rows for {test_month}: {len(filtered)}")

filtered = filtered[filtered['provider_key'] == test_provider]
print(f"Rows for {test_month} + {test_provider}: {len(filtered)}")
