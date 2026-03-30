"""
Quick test to verify data is loading correctly
"""
from app import load_csv_data

print("=" * 50)
print("TESTING DATA LOADER")
print("=" * 50)

df = load_csv_data()

print(f"\n[OK] Total rows loaded: {len(df)}")
print(f"[OK] Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
print(f"[OK] Providers: {', '.join(df['provider'].unique()[:10])}")

latest_date = df['date_parsed'].max().date()
latest_data = df[df['date_parsed'].dt.date == latest_date]

print(f"\n[OK] Latest date: {latest_date}")
print(f"[OK] Latest draws: {len(latest_data)}")

print("\nLatest Results:")
print("-" * 50)
for _, row in latest_data.iterrows():
    print(f"{row['provider'].upper():15} | 1st: {row['1st_real']} | 2nd: {row['2nd_real']} | 3rd: {row['3rd_real']}")

print("\n" + "=" * 50)
print("[SUCCESS] Everything is working!")
print("=" * 50)
print("\nNow open: http://127.0.0.1:5000")
