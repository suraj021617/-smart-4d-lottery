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
    
    # Convert date column properly
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    
    # Check latest data
    latest_date = df['date'].max()
    print(f"[OK] Latest date in CSV: {latest_date.strftime('%Y-%m-%d')}")
    
    # Show first few entries to understand structure
    print("\n=== SAMPLE DATA ===")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        print(f"Date: {row['date'].strftime('%Y-%m-%d')} | Provider: {row['provider'].split('/')[-1]} | 1st: {row['1st']}")
    
    # Separate different lottery types based on number formats and draw_info
    def categorize_lottery_type(row):
        """Categorize lottery type based on draw_info and 1st prize numbers"""
        draw_info = str(row['draw_info']).strip()
        first_prize = str(row['1st']).strip()
        
        # Check draw_info for explicit type
        if '5D 6D' in draw_info or '6D' in draw_info:
            return '5D_6D'
        elif '4D' in draw_info:
            return '4D'
        elif '3D' in draw_info:
            return '3D'
        
        # Extract numbers from first prize text
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
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
        if ltype in df['lottery_type'].values:
            latest_entries = df[df['lottery_type'] == ltype].sort_values('date').tail(3)
            if not latest_entries.empty:
                print(f"\n{ltype} Latest entries:")
                for _, row in latest_entries.iterrows():
                    provider = row['provider'].split('/')[-1] if '/' in str(row['provider']) else str(row['provider'])
                    print(f"  {row['date'].strftime('%Y-%m-%d')} | {provider} | {row['1st']}")
    
    # Check for data up to 2025-07-16
    target_date = datetime(2025, 7, 16)
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        print(f"\n[WARNING] Missing {missing_days} days of data (up to 2025-07-16)")
    else:
        print(f"\n[OK] Data is up to date (latest: {latest_date.strftime('%Y-%m-%d')})")
    
    # Create separate datasets for each lottery type
    datasets = {}
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
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
    create_summary_report(datasets, df)
    
    return True

def create_summary_report(datasets, original_df):
    """Create a summary report of the lottery data"""
    
    report = []
    report.append("=== LOTTERY SYSTEM ANALYSIS REPORT ===")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append(f"Total entries in original CSV: {len(original_df)}")
    report.append(f"Date range: {original_df['date'].min().strftime('%Y-%m-%d')} to {original_df['date'].max().strftime('%Y-%m-%d')}")
    report.append("")
    
    for ltype, data in datasets.items():
        if len(data) > 0:
            report.append(f"=== {ltype} LOTTERY ===")
            report.append(f"Total entries: {len(data)}")
            report.append(f"Date range: {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
            
            # Provider distribution
            providers = data['provider'].value_counts()
            report.append("Top providers:")
            for provider, count in providers.head(3).items():
                clean_provider = provider.replace('https://www.live4d2u.net/images/', '').title()
                report.append(f"  - {clean_provider}: {count} entries")
            
            # Recent entries
            report.append("Recent entries:")
            recent = data.tail(3)
            for _, row in recent.iterrows():
                clean_provider = row['provider'].replace('https://www.live4d2u.net/images/', '').title()
                report.append(f"  - {row['date'].strftime('%Y-%m-%d')}: {clean_provider} | {row['1st']}")
            
            report.append("")
    
    # Issues found
    report.append("=== ISSUES IDENTIFIED ===")
    
    # Check if data goes to 2025-07-16
    latest_date = original_df['date'].max()
    target_date = datetime(2025, 7, 16)
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        report.append(f"1. MISSING DATA: {missing_days} days missing (latest: {latest_date.strftime('%Y-%m-%d')}, target: 2025-07-16)")
    else:
        report.append("1. DATA COMPLETENESS: OK - Data is up to target date")
    
    # Check mixed number formats
    report.append("2. MIXED NUMBER FORMATS: Different lottery types (4D, 5D, 6D) are mixed in same dataset")
    report.append("   - This causes prediction confusion")
    report.append("   - Solution: Use separate datasets for each type")
    
    # Check prediction accuracy
    report.append("3. PREDICTION ACCURACY: System shows wrong predictions due to mixed data")
    report.append("   - Solution: Create separate prediction buttons for each lottery type")
    
    report.append("")
    report.append("=== RECOMMENDED FIXES ===")
    report.append("1. Update app.py to use separate CSV files for each lottery type")
    report.append("2. Create separate prediction buttons: '4D Predictions', '5D Predictions', '6D Predictions'")
    report.append("3. Fix date parsing to read all data up to 2025-07-16")
    report.append("4. Update prediction algorithms to work with specific number formats")
    
    # Save report
    with open('lottery_analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print("[OK] Created lottery_analysis_report.txt")

if __name__ == "__main__":
    success = fix_lottery_system()
    if success:
        print("\n[SUCCESS] LOTTERY SYSTEM ANALYSIS COMPLETED!")
        print("\nFiles created:")
        print("- 4d_results_history.csv (4D numbers only)")
        print("- 5d_results_history.csv (5D numbers only)")  
        print("- 6d_results_history.csv (6D numbers only)")
        print("- 5d_6d_results_history.csv (5D/6D mixed)")
        print("- lottery_analysis_report.txt (detailed analysis)")
        print("\nNext steps:")
        print("1. Update your app.py to use separate datasets")
        print("2. Create separate prediction buttons for each lottery type")
        print("3. Fix the date parsing issue")
    else:
        print("\n[ERROR] Failed to analyze lottery system")