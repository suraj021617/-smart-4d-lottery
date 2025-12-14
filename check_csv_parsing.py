"""
Quick CSV Data Parsing Check
"""
import pandas as pd
import re
from collections import Counter

def check_csv_parsing():
    """Check if CSV data is parsing correctly"""
    
    # Try to load CSV
    try:
        df = pd.read_csv('4d_results_history.csv', index_col=False, on_bad_lines='skip')
        print(f"✅ CSV loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
        return
    
    # Check first few rows
    print("\n📋 First 3 rows:")
    print(df.head(3).to_string())
    
    # Check date parsing
    try:
        df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
        valid_dates = df['date_parsed'].notna().sum()
        print(f"\n📅 Date parsing: {valid_dates}/{len(df)} valid dates")
        if valid_dates > 0:
            print(f"   Date range: {df['date_parsed'].min()} to {df['date_parsed'].max()}")
    except Exception as e:
        print(f"❌ Date parsing failed: {e}")
    
    # Check provider data
    try:
        providers = df['provider'].dropna().unique()
        print(f"\n🏢 Providers found: {len(providers)}")
        for p in providers[:5]:
            print(f"   - {p}")
    except Exception as e:
        print(f"❌ Provider check failed: {e}")
    
    # Check prize data extraction
    print("\n🎯 Testing prize number extraction:")
    
    # Method 1: Check if prize_text column exists
    if 'prize_text' in df.columns:
        print("   ✅ prize_text column found")
        sample_prize = df['prize_text'].dropna().iloc[0] if not df['prize_text'].dropna().empty else ""
        print(f"   Sample: {sample_prize[:100]}...")
    elif '3rd' in df.columns:
        print("   ✅ Using '3rd' column as prize_text")
        sample_prize = df['3rd'].dropna().iloc[0] if not df['3rd'].dropna().empty else ""
        print(f"   Sample: {sample_prize[:100]}...")
    else:
        print("   ❌ No prize text column found")
        return
    
    # Method 2: Test number extraction
    extracted_numbers = []
    for i, row in df.head(10).iterrows():
        prize_text = str(row.get('prize_text', ''))
        if not prize_text or prize_text == 'nan':
            prize_text = str(row.get('3rd', ''))
        
        # Extract numbers
        first_match = re.search(r'1st\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        second_match = re.search(r'2nd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        third_match = re.search(r'3rd\s+Prize[^\d]*(\d{4})', prize_text, re.IGNORECASE)
        
        row_numbers = []
        if first_match:
            row_numbers.append(('1st', first_match.group(1)))
        if second_match:
            row_numbers.append(('2nd', second_match.group(1)))
        if third_match:
            row_numbers.append(('3rd', third_match.group(1)))
        
        if row_numbers:
            extracted_numbers.extend([num for _, num in row_numbers])
            print(f"   Row {i}: {row_numbers}")
    
    # Summary
    print(f"\n📈 Extraction Summary:")
    print(f"   Total numbers extracted: {len(extracted_numbers)}")
    if extracted_numbers:
        print(f"   Sample numbers: {extracted_numbers[:10]}")
        freq = Counter(extracted_numbers)
        print(f"   Most common: {freq.most_common(5)}")
    else:
        print("   ❌ No numbers extracted - check regex patterns")
    
    # Alternative extraction methods
    print(f"\n🔍 Alternative extraction methods:")
    
    # Try direct column extraction
    for col in ['1st', '2nd', '3rd', '1st_real', '2nd_real', '3rd_real']:
        if col in df.columns:
            valid_nums = [n for n in df[col].astype(str) if len(n) == 4 and n.isdigit()]
            print(f"   {col}: {len(valid_nums)} valid 4D numbers")
    
    # Try regex on all text columns
    all_4d_numbers = []
    for col in df.columns:
        if df[col].dtype == 'object':
            for val in df[col].astype(str).dropna()[:20]:
                found = re.findall(r'\b\d{4}\b', str(val))
                all_4d_numbers.extend(found)
    
    print(f"   Regex on all columns: {len(all_4d_numbers)} 4D numbers found")
    if all_4d_numbers:
        print(f"   Sample: {all_4d_numbers[:10]}")

if __name__ == "__main__":
    check_csv_parsing()