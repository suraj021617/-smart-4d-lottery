"""
CSV Data Validator - Check 4d_results_history.csv for issues
"""
import pandas as pd
import re

def validate_csv():
    print("[CHECK] Validating 4d_results_history.csv...")
    print("=" * 60)
    
    try:
        df = pd.read_csv('4d_results_history.csv', on_bad_lines='skip')
        print(f"[OK] Loaded {len(df)} rows\n")
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return
    
    issues = []
    
    # Check 1: Column structure
    print("[1] Checking columns...")
    expected_cols = ['date', 'provider', 'draw_info', 'prizes']
    if len(df.columns) < 4:
        issues.append(f"⚠️ Only {len(df.columns)} columns found")
    print(f"   Columns: {list(df.columns)[:5]}")
    
    # Check 2: Date parsing
    print("\n[2] Checking dates...")
    try:
        df['date_parsed'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
        invalid_dates = df['date_parsed'].isna().sum()
        if invalid_dates > 0:
            issues.append(f"[WARN] {invalid_dates} invalid dates")
        print(f"   Valid dates: {len(df) - invalid_dates}/{len(df)}")
        print(f"   Range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")
    except Exception as e:
        issues.append(f"❌ Date parsing failed: {e}")
    
    # Check 3: Extract 4D numbers
    print("\n[3] Checking 4D numbers...")
    total_4d = 0
    rows_with_4d = 0
    
    for idx, row in df.head(100).iterrows():
        row_str = ' '.join([str(val) for val in row if pd.notna(val)])
        numbers = re.findall(r'\b\d{4}\b', row_str)
        valid_4d = [n for n in numbers if n != '----']
        
        if valid_4d:
            rows_with_4d += 1
            total_4d += len(valid_4d)
    
    print(f"   Rows with 4D: {rows_with_4d}/100 (sample)")
    print(f"   Total 4D found: {total_4d}")
    
    if rows_with_4d < 50:
        issues.append(f"[WARN] Low 4D extraction rate: {rows_with_4d}%")
    
    # Check 4: Provider detection
    print("\n[4] Checking providers...")
    providers = set()
    for idx, row in df.head(100).iterrows():
        row_str = str(row.iloc[1]) if len(row) > 1 else ''
        if 'magnum' in row_str.lower():
            providers.add('Magnum')
        elif 'damacai' in row_str.lower() or 'da ma cai' in row_str.lower():
            providers.add('Da Ma Cai')
        elif 'toto' in row_str.lower() or 'sports' in row_str.lower():
            providers.add('Sports Toto')
        elif 'singapore' in row_str.lower():
            providers.add('Singapore')
        elif 'grand dragon' in row_str.lower() or 'gdlotto' in row_str.lower():
            providers.add('Grand Dragon')
    
    print(f"   Providers found: {', '.join(sorted(providers))}")
    if len(providers) < 3:
        issues.append(f"[WARN] Only {len(providers)} providers detected")
    
    # Check 5: Data quality
    print("\n[5] Checking data quality...")
    
    # Empty rows
    empty_rows = df.isna().all(axis=1).sum()
    if empty_rows > 0:
        issues.append(f"[WARN] {empty_rows} completely empty rows")
    
    # Duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"[WARN] {duplicates} duplicate rows")
    
    print(f"   Empty rows: {empty_rows}")
    print(f"   Duplicates: {duplicates}")
    
    # Check 6: Sample data
    print("\n[6] Sample data (first 3 rows):")
    for idx, row in df.head(3).iterrows():
        date = row.iloc[0] if len(row) > 0 else 'N/A'
        provider = str(row.iloc[1])[:30] if len(row) > 1 else 'N/A'
        prizes = str(row.iloc[4])[:50] if len(row) > 4 else 'N/A'
        
        # Extract 4D numbers
        numbers = re.findall(r'\b\d{4}\b', prizes)
        valid = [n for n in numbers if n != '----'][:3]
        
        print(f"\n   Row {idx}:")
        print(f"   Date: {date}")
        print(f"   Provider: {provider}")
        print(f"   4D Numbers: {', '.join(valid) if valid else 'None found'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    if not issues:
        print("[OK] No major issues found!")
        print("\nYour CSV data looks good:")
        print(f"   • {len(df)} total rows")
        print(f"   • {len(providers)} providers detected")
        print(f"   • {total_4d} 4D numbers in sample")
        print(f"   • Date range: {df['date_parsed'].min().date()} to {df['date_parsed'].max().date()}")
    else:
        print("[WARN] Issues found:")
        for issue in issues:
            print(f"   {issue}")
        
        print("\n[FIX] Recommendations:")
        if any('date' in i.lower() for i in issues):
            print("   • Check date format (should be YYYY-MM-DD)")
        if any('4d' in i.lower() for i in issues):
            print("   • Verify prize column contains 4D numbers")
        if any('provider' in i.lower() for i in issues):
            print("   • Check provider names in column 2")
    
    print("=" * 60)
    
    # Quick fix suggestions
    print("\n[INFO] Quick Fixes Available:")
    print("   1. Run: python clean_csv.py (if exists)")
    print("   2. Check: utils/data_normalizer.py")
    print("   3. Test: python test_optimizations.py")

if __name__ == '__main__':
    validate_csv()
