import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def fix_lottery_system():
    """
    Fix the lottery system to properly handle different number formats
    and parse the latest data correctly
    """
    
    print("=== FIXING LOTTERY SYSTEM ===")
    
    # Load the CSV data
    try:
        df = pd.read_csv('4d_results_history.csv')
        print(f"[OK] Loaded CSV with {len(df)} rows")
    except Exception as e:
        print(f"[ERROR] Error loading CSV: {e}")
        return False
    
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Check latest data
    latest_date = df['date'].max()
    print(f"[OK] Latest date in CSV: {latest_date.strftime('%Y-%m-%d')}")
    
    # Separate different lottery types based on number formats
    def categorize_lottery_type(row):
        """Categorize lottery type based on the numbers in 1st prize"""
        first_prize = str(row['1st']).strip()
        
        # Extract numbers from the text
        numbers = re.findall(r'\d+', first_prize)
        if not numbers:
            return 'Unknown'
        
        # Get the main winning number (usually the first one)
        main_number = numbers[0]
        
        # Determine type based on number length
        if len(main_number) == 4:
            return '4D'
        elif len(main_number) == 5:
            return '5D'
        elif len(main_number) == 6:
            return '6D'
        elif len(main_number) == 3:
            return '3D'
        else:
            return 'Other'
    
    # Add lottery type column
    df['lottery_type'] = df.apply(categorize_lottery_type, axis=1)
    
    # Show distribution of lottery types
    print("\n=== LOTTERY TYPE DISTRIBUTION ===")
    type_counts = df['lottery_type'].value_counts()
    for ltype, count in type_counts.items():
        print(f"{ltype}: {count} entries")
    
    # Show latest entries by type
    print("\n=== LATEST ENTRIES BY TYPE ===")
    for ltype in ['4D', '5D', '6D', '3D']:
        if ltype in df['lottery_type'].values:
            latest_entry = df[df['lottery_type'] == ltype].sort_values('date').tail(1)
            if not latest_entry.empty:
                row = latest_entry.iloc[0]
                print(f"{ltype}: {row['date'].strftime('%Y-%m-%d')} | {row['provider']} | {row['1st']}")
    
    # Check for data up to 2025-07-16
    target_date = datetime(2025, 7, 16)
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        print(f"\n[WARNING] Missing {missing_days} days of data (up to 2025-07-16)")
    else:
        print(f"\n[OK] Data is up to date (latest: {latest_date.strftime('%Y-%m-%d')})")
    
    # Create separate datasets for each lottery type
    datasets = {}
    for ltype in ['4D', '5D', '6D', '3D']:
        if ltype in df['lottery_type'].values:
            datasets[ltype] = df[df['lottery_type'] == ltype].copy()
            datasets[ltype] = datasets[ltype].sort_values('date')
            print(f"[OK] Created {ltype} dataset with {len(datasets[ltype])} entries")
    
    # Save separate CSV files for each type
    for ltype, data in datasets.items():
        filename = f"{ltype.lower()}_results_history.csv"
        data.to_csv(filename, index=False)
        print(f"[OK] Saved {filename}")
    
    # Create a summary report
    create_summary_report(datasets)
    
    return True

def create_summary_report(datasets):
    """Create a summary report of the lottery data"""
    
    report = []
    report.append("=== LOTTERY SYSTEM ANALYSIS REPORT ===")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    for ltype, data in datasets.items():
        if len(data) > 0:
            report.append(f"=== {ltype} LOTTERY ===")
            report.append(f"Total entries: {len(data)}")
            report.append(f"Date range: {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
            
            # Provider distribution
            providers = data['provider'].value_counts()
            report.append("Providers:")
            for provider, count in providers.head(5).items():
                clean_provider = provider.replace('https://www.live4d2u.net/images/', '').title()
                report.append(f"  - {clean_provider}: {count} entries")
            
            # Recent entries
            report.append("Recent entries:")
            recent = data.tail(3)
            for _, row in recent.iterrows():
                clean_provider = row['provider'].replace('https://www.live4d2u.net/images/', '').title()
                report.append(f"  - {row['date'].strftime('%Y-%m-%d')}: {clean_provider} | {row['1st']}")
            
            report.append("")
    
    # Save report
    with open('lottery_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("[OK] Created lottery_analysis_report.txt")

if __name__ == "__main__":
    success = fix_lottery_system()
    if success:
        print("\n[SUCCESS] LOTTERY SYSTEM FIXED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Update your app.py to use separate datasets for 4D, 5D, 6D")
        print("2. Create separate prediction buttons for each lottery type")
        print("3. Fix the date parsing to read up to 2025-07-16")
    else:
        print("\n❌ Failed to fix lottery system")