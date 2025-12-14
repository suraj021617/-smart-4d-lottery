import pandas as pd
from datetime import datetime, timedelta

def check_data_issues():
    try:
        # Load CSV
        df = pd.read_csv('4d_results_history.csv')
        print(f"CSV loaded successfully: {len(df)} rows")
        
        # Check columns
        print(f"Columns: {list(df.columns)}")
        
        # Check date range
        df['Date'] = pd.to_datetime(df['Date'])
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        
        # Check latest 10 entries
        print("\n=== LATEST 10 ENTRIES ===")
        latest = df.tail(10)
        for _, row in latest.iterrows():
            print(f"{row['Date'].strftime('%Y-%m-%d')} | {row['Provider']} | {row['Numbers']}")
        
        # Check providers and number formats
        print(f"\n=== PROVIDERS ===")
        providers = df['Provider'].value_counts()
        for provider, count in providers.items():
            print(f"{provider}: {count} entries")
            
        # Check number formats by provider
        print(f"\n=== NUMBER FORMATS BY PROVIDER ===")
        for provider in df['Provider'].unique():
            provider_data = df[df['Provider'] == provider]
            sample_numbers = provider_data['Numbers'].head(3).tolist()
            print(f"{provider}: {sample_numbers}")
            
        # Check if data goes to 2025-07-16
        target_date = datetime(2025, 7, 16)
        max_date = df['Date'].max()
        print(f"\nTarget date (2025-07-16): {target_date.date()}")
        print(f"Latest date in CSV: {max_date.date()}")
        print(f"Missing days: {(target_date - max_date).days}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_data_issues()