import pandas as pd
import re
from datetime import datetime

def fix_csv_structure():
    """
    Fix the CSV structure and extract the correct winning numbers
    """
    
    print("=== FIXING CSV STRUCTURE ===")
    
    # Load the CSV
    df = pd.read_csv('4d_results_history.csv')
    print(f"[OK] Loaded {len(df)} rows")
    
    # Show the actual structure
    print("\n=== ACTUAL CSV STRUCTURE ===")
    print("Columns:", list(df.columns))
    
    # Show sample row
    sample = df.iloc[0]
    print(f"\nSample row:")
    for col in df.columns:
        print(f"  {col}: {sample[col]}")
    
    # The winning numbers are actually in the '2nd' column!
    # Let's extract them properly
    
    def extract_winning_numbers(text):
        """Extract winning numbers from the text"""
        if pd.isna(text):
            return {'1st': '', '2nd': '', '3rd': ''}
        
        text = str(text)
        
        # Look for patterns like "1st Prize 首獎 4529"
        first_match = re.search(r'1st Prize 首獎 (\d+)', text)
        second_match = re.search(r'2nd Prize 二獎 (\d+)', text)
        third_match = re.search(r'3rd Prize 三獎 (\d+)', text)
        
        # Also look for patterns like "1st 首獎 2199"
        if not first_match:
            first_match = re.search(r'1st 首獎 (\d+)', text)
        if not second_match:
            second_match = re.search(r'2nd 二獎 (\d+)', text)
        if not third_match:
            third_match = re.search(r'3rd 三獎 (\d+)', text)
        
        # For 5D/6D numbers, look for different patterns
        if not first_match:
            # Pattern like "1st 98894 4th 8894"
            first_match = re.search(r'1st (\d{4,6})', text)
        
        return {
            '1st': first_match.group(1) if first_match else '',
            '2nd': second_match.group(1) if second_match else '',
            '3rd': third_match.group(1) if third_match else ''
        }
    
    # Extract winning numbers from the correct column
    print("\n=== EXTRACTING WINNING NUMBERS ===")
    
    # The winning numbers are in the '2nd' column (which is actually the 5th column)
    winning_data = []
    
    for idx, row in df.iterrows():
        # Extract date
        date_str = row['date']
        
        # Extract provider
        provider = row['provider']
        
        # Extract lottery type from draw_info
        draw_info = str(row['draw_info'])
        
        # Extract winning numbers from the '2nd' column
        winning_text = str(row['2nd'])
        numbers = extract_winning_numbers(winning_text)
        
        # Determine lottery type
        lottery_type = '4D'  # default
        if '5D 6D' in draw_info or '6D' in draw_info:
            lottery_type = '5D_6D'
        elif '5D' in draw_info:
            lottery_type = '5D'
        elif '3D' in draw_info:
            lottery_type = '3D'
        
        winning_data.append({
            'date': date_str,
            'provider': provider,
            'lottery_type': lottery_type,
            'draw_info': draw_info,
            'first_prize': numbers['1st'],
            'second_prize': numbers['2nd'],
            'third_prize': numbers['3rd'],
            'original_text': winning_text
        })
        
        if idx < 5:  # Show first 5 for debugging
            print(f"Row {idx}: {date_str} | {lottery_type} | 1st: {numbers['1st']}")
    
    # Create new DataFrame
    new_df = pd.DataFrame(winning_data)
    
    # Convert dates
    new_df['date'] = pd.to_datetime(new_df['date'], format='%Y-%m-%d', errors='coerce')
    
    # Remove rows with invalid dates or empty winning numbers
    new_df = new_df[new_df['date'].notna()]
    new_df = new_df[new_df['first_prize'] != '']
    
    print(f"\n[OK] Processed {len(new_df)} valid entries")
    print(f"Date range: {new_df['date'].min().strftime('%Y-%m-%d')} to {new_df['date'].max().strftime('%Y-%m-%d')}")
    
    # Show lottery type distribution
    print(f"\n=== LOTTERY TYPE DISTRIBUTION ===")
    type_counts = new_df['lottery_type'].value_counts()
    for ltype, count in type_counts.items():
        print(f"{ltype}: {count} entries")
    
    # Show recent entries by type
    print(f"\n=== RECENT ENTRIES BY TYPE ===")
    for ltype in ['4D', '5D', '6D', '5D_6D', '3D']:
        if ltype in new_df['lottery_type'].values:
            recent = new_df[new_df['lottery_type'] == ltype].nlargest(3, 'date')
            if not recent.empty:
                print(f"\n{ltype}:")
                for _, row in recent.iterrows():
                    provider = row['provider'].split('/')[-1] if '/' in row['provider'] else row['provider']
                    print(f"  {row['date'].strftime('%Y-%m-%d')} | {provider} | {row['first_prize']}")
    
    # Save the corrected data
    new_df.to_csv('corrected_lottery_data.csv', index=False)
    print(f"\n[OK] Saved corrected data to 'corrected_lottery_data.csv'")
    
    # Create separate files by lottery type
    print(f"\n=== CREATING SEPARATE FILES ===")
    for ltype in type_counts.index:
        type_data = new_df[new_df['lottery_type'] == ltype].copy()
        filename = f"{ltype.lower()}_lottery_data.csv"
        type_data.to_csv(filename, index=False)
        print(f"[OK] Created {filename} with {len(type_data)} entries")
    
    # Check for latest data
    latest_date = new_df['date'].max()
    target_date = datetime(2025, 7, 16)
    
    print(f"\n=== DATA COMPLETENESS ===")
    print(f"Latest date: {latest_date.strftime('%Y-%m-%d')}")
    print(f"Target date: 2025-07-16")
    
    if latest_date < target_date:
        missing_days = (target_date - latest_date).days
        print(f"[WARNING] Missing {missing_days} days of data")
    else:
        print(f"[OK] Data is up to date")
    
    return True

if __name__ == "__main__":
    success = fix_csv_structure()
    if success:
        print(f"\n[SUCCESS] CSV STRUCTURE FIXED!")
        print(f"\nFiles created:")
        print(f"- corrected_lottery_data.csv (all data with proper structure)")
        print(f"- 4d_lottery_data.csv (4D numbers only)")
        print(f"- 5d_lottery_data.csv (5D numbers only)")
        print(f"- 6d_lottery_data.csv (6D numbers only)")
        print(f"- 5d_6d_lottery_data.csv (5D/6D mixed)")
        print(f"\nNow you can:")
        print(f"1. Update app.py to use the correct CSV files")
        print(f"2. Create separate prediction buttons for each lottery type")
        print(f"3. Fix the date parsing issue")
    else:
        print(f"\n[ERROR] Failed to fix CSV structure")