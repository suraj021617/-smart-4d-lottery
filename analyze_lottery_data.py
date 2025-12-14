import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

def analyze_lottery_data():
    """
    Analyze the lottery data to understand the issues and create separate datasets
    """
    
    print("=== ANALYZING LOTTERY DATA ===")
    
    # Load the CSV data
    try:
        df = pd.read_csv('4d_results_history.csv')
        print(f"[OK] Loaded CSV with {len(df)} rows")
        print(f"[OK] Columns: {list(df.columns)}")
    except Exception as e:
        print(f"[ERROR] Error loading CSV: {e}")
        return False
    
    # Check date column
    print(f"\n=== DATE ANALYSIS ===")
    print(f"Sample dates: {df['date'].head().tolist()}")
    
    # Try to convert dates
    df['date_converted'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    
    # Check for invalid dates
    invalid_dates = df[df['date_converted'].isna()]
    print(f"Invalid dates found: {len(invalid_dates)}")
    if len(invalid_dates) > 0:
        print("Sample invalid dates:")
        for i in range(min(3, len(invalid_dates))):
            print(f"  - {invalid_dates.iloc[i]['date']}")
    
    # Use valid dates only
    df_valid = df[df['date_converted'].notna()].copy()
    df_valid['date'] = df_valid['date_converted']
    
    latest_date = df_valid['date'].max()
    earliest_date = df_valid['date'].min()
    print(f"[OK] Valid date range: {earliest_date.strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
    print(f"[OK] Valid entries: {len(df_valid)}")
    
    # Show sample data structure
    print(f"\n=== SAMPLE DATA STRUCTURE ===")
    for i in range(min(5, len(df_valid))):
        row = df_valid.iloc[i]
        provider = str(row['provider']).split('/')[-1] if '/' in str(row['provider']) else str(row['provider'])
        print(f"Date: {row['date'].strftime('%Y-%m-%d')} | Provider: {provider}")
        print(f"  Draw Info: {row['draw_info']}")
        print(f"  1st Prize: {row['1st']}")
        print()
    
    # Categorize lottery types
    def get_lottery_type(row):
        """Determine lottery type from draw_info and 1st prize"""
        draw_info = str(row['draw_info']).upper()
        first_prize = str(row['1st'])
        
        # Check draw_info for explicit mentions
        if '5D 6D' in draw_info or ('5D' in draw_info and '6D' in draw_info):
            return '5D_6D'
        elif '6D' in draw_info:
            return '6D'
        elif '5D' in draw_info:
            return '5D'
        elif '4D' in draw_info:
            return '4D'
        elif '3D' in draw_info:
            return '3D'
        
        # Extract numbers from first prize
        numbers = re.findall(r'\b\d{3,6}\b', first_prize)
        if numbers:
            main_number = numbers[0]
            if len(main_number) == 6:
                return '6D'
            elif len(main_number) == 5:
                return '5D'
            elif len(main_number) == 4:
                return '4D'
            elif len(main_number) == 3:
                return '3D'
        
        return 'Unknown'
    
    # Add lottery type
    df_valid['lottery_type'] = df_valid.apply(get_lottery_type, axis=1)
    
    # Show distribution
    print(f"=== LOTTERY TYPE DISTRIBUTION ===")
    type_counts = df_valid['lottery_type'].value_counts()
    for ltype, count in type_counts.items():
        percentage = (count / len(df_valid)) * 100
        print(f"{ltype}: {count} entries ({percentage:.1f}%)")
    
    # Show recent entries by type
    print(f"\n=== RECENT ENTRIES BY TYPE ===")
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
        if ltype in df_valid['lottery_type'].values:
            recent = df_valid[df_valid['lottery_type'] == ltype].nlargest(3, 'date')
            if not recent.empty:
                print(f"\n{ltype} (Latest 3 entries):")
                for _, row in recent.iterrows():
                    provider = str(row['provider']).split('/')[-1] if '/' in str(row['provider']) else str(row['provider'])
                    print(f"  {row['date'].strftime('%Y-%m-%d')} | {provider} | {row['1st']}")
    
    # Check data completeness
    print(f"\n=== DATA COMPLETENESS CHECK ===")
    target_date = datetime(2025, 7, 16)
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        print(f"[WARNING] Missing {missing_days} days of data")
        print(f"Latest: {latest_date.strftime('%Y-%m-%d')}, Target: 2025-07-16")
    else:
        print(f"[OK] Data is complete up to target date")
    
    # Create separate datasets
    print(f"\n=== CREATING SEPARATE DATASETS ===")
    datasets_created = 0
    
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
        if ltype in df_valid['lottery_type'].values:
            type_data = df_valid[df_valid['lottery_type'] == ltype].copy()
            type_data = type_data.sort_values('date')
            
            # Save to separate file
            filename = f"{ltype.lower()}_results.csv"
            type_data.to_csv(filename, index=False)
            
            print(f"[OK] Created {filename} with {len(type_data)} entries")
            print(f"     Date range: {type_data['date'].min().strftime('%Y-%m-%d')} to {type_data['date'].max().strftime('%Y-%m-%d')}")
            datasets_created += 1
    
    # Create analysis report
    create_analysis_report(df_valid, type_counts, latest_date, target_date)
    
    return datasets_created > 0

def create_analysis_report(df_valid, type_counts, latest_date, target_date):
    """Create detailed analysis report"""
    
    report = []
    report.append("=== LOTTERY SYSTEM ANALYSIS REPORT ===")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Summary
    report.append("=== SUMMARY ===")
    report.append(f"Total valid entries: {len(df_valid):,}")
    report.append(f"Date range: {df_valid['date'].min().strftime('%Y-%m-%d')} to {latest_date.strftime('%Y-%m-%d')}")
    report.append("")
    
    # Lottery types
    report.append("=== LOTTERY TYPES FOUND ===")
    for ltype, count in type_counts.items():
        percentage = (count / len(df_valid)) * 100
        report.append(f"{ltype}: {count:,} entries ({percentage:.1f}%)")
    report.append("")
    
    # Issues identified
    report.append("=== ISSUES IDENTIFIED ===")
    
    # Data completeness
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        report.append(f"1. MISSING DATA: {missing_days} days missing")
        report.append(f"   Latest: {latest_date.strftime('%Y-%m-%d')}, Expected: 2025-07-16")
    else:
        report.append("1. DATA COMPLETENESS: OK")
    
    # Mixed formats
    report.append("2. MIXED NUMBER FORMATS: Multiple lottery types in same dataset")
    report.append("   - 4D numbers (4 digits): GDLotto style")
    report.append("   - 5D numbers (5 digits): SportsToto style") 
    report.append("   - 6D numbers (6 digits): Da Ma Cai style")
    report.append("   - This causes prediction confusion")
    
    # Prediction issues
    report.append("3. PREDICTION SYSTEM ISSUES:")
    report.append("   - System treats all numbers as 4D")
    report.append("   - 5D/6D numbers get truncated or misprocessed")
    report.append("   - Predictions show wrong format numbers")
    
    report.append("")
    report.append("=== RECOMMENDED SOLUTIONS ===")
    report.append("1. SEPARATE DATASETS: Use individual CSV files for each lottery type")
    report.append("2. SEPARATE UI: Create different prediction buttons:")
    report.append("   - '4D Predictions' (GDLotto)")
    report.append("   - '5D Predictions' (SportsToto 5D)")
    report.append("   - '6D Predictions' (Da Ma Cai)")
    report.append("3. UPDATE ALGORITHMS: Modify prediction logic for each number format")
    report.append("4. FIX DATE PARSING: Ensure system reads all data up to 2025-07-16")
    
    report.append("")
    report.append("=== FILES CREATED ===")
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
        if ltype in type_counts:
            report.append(f"- {ltype.lower()}_results.csv ({type_counts[ltype]:,} entries)")
    
    # Save report
    with open('lottery_system_analysis.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"[OK] Created lottery_system_analysis.txt")

if __name__ == "__main__":
    success = analyze_lottery_data()
    if success:
        print(f"\n[SUCCESS] ANALYSIS COMPLETED!")
        print(f"\nSeparate datasets created for each lottery type.")
        print(f"Check 'lottery_system_analysis.txt' for detailed report.")
        print(f"\nTo fix your system:")
        print(f"1. Use separate CSV files for each lottery type")
        print(f"2. Create separate prediction buttons")
        print(f"3. Update app.py to handle different number formats")
    else:
        print(f"\n[ERROR] Analysis failed")