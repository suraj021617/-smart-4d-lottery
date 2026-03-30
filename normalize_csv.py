"""
CSV Normalization Script - Converts messy CSV to clean normalized format
SAFE: Creates NEW file, doesn't touch original
"""
import pandas as pd
import re
from datetime import datetime

def extract_4d_numbers(text):
    """Extract only 4D numbers (0000-9999)"""
    if pd.isna(text) or text == '':
        return []
    matches = re.findall(r'\b\d{4}\b', str(text))
    return [m for m in matches if len(m) == 4 and m.isdigit()]

def normalize_provider(provider_text):
    """Normalize provider name"""
    if pd.isna(provider_text):
        return ''
    provider = str(provider_text).lower()
    if 'magnum' in provider:
        return 'magnum'
    elif 'damacai' in provider or 'dmc' in provider:
        return 'damacai'
    elif 'toto' in provider or 'sports' in provider:
        return 'toto'
    elif 'gdlotto' in provider or 'grand' in provider:
        return 'gdlotto'
    elif 'singapore' in provider:
        return 'singapore'
    elif 'sandakan' in provider:
        return 'sandakan'
    elif 'cashsweep' in provider:
        return 'cashsweep'
    elif 'sabah' in provider:
        return 'sabah88'
    elif 'perdana' in provider:
        return 'perdana'
    elif 'harihari' in provider:
        return 'harihari'
    else:
        # Extract from URL pattern
        match = re.search(r'images/([^/\s,]+)', provider)
        if match:
            return match.group(1).strip().lower()
        return provider.strip().lower()

def detect_game_type(row):
    """Detect game type from row data"""
    draw_details = str(row.get('3rd', ''))
    
    if '5D' in draw_details or '6D' in draw_details:
        return '5D 6D Lotto'
    elif 'Jackpot Gold' in draw_details:
        return 'Jackpot Gold'
    elif 'Magnum Life' in draw_details:
        return 'Magnum Life'
    elif 'Toto' in draw_details:
        return 'Toto'
    elif '3+3D' in draw_details:
        return '3+3D'
    else:
        return '4D Jackpot'

def extract_prizes(row):
    """Extract 1st, 2nd, 3rd prize from text"""
    prize_text = str(row.get('3rd', ''))
    
    prizes = {'1st': '', '2nd': '', '3rd': ''}
    
    # Extract 1st Prize
    first_match = re.search(r'1st[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
    if first_match:
        prizes['1st'] = first_match.group(1)
    
    # Extract 2nd Prize
    second_match = re.search(r'2nd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
    if second_match:
        prizes['2nd'] = second_match.group(1)
    
    # Extract 3rd Prize
    third_match = re.search(r'3rd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
    if third_match:
        prizes['3rd'] = third_match.group(1)
    
    return prizes

def normalize_csv(input_file='4d_results_history.csv', output_file='4d_results_normalized.csv'):
    """
    Main normalization function
    """
    print("[*] Starting CSV normalization...")
    print(f"[*] Reading: {input_file}")
    
    try:
        # Read original CSV
        df = pd.read_csv(input_file, index_col=False, on_bad_lines='skip')
        print(f"[OK] Loaded {len(df)} rows")
        
        # Create normalized structure
        normalized_rows = []
        
        for idx, row in df.iterrows():
            try:
                # Parse date
                date_val = None
                for col in ['date', 'Date', df.columns[0]]:
                    if col in df.columns:
                        try:
                            date_val = pd.to_datetime(row[col], errors='coerce')
                            if pd.notna(date_val):
                                break
                        except:
                            continue
                
                if pd.isna(date_val):
                    continue
                
                # Normalize provider
                provider = normalize_provider(row.get('provider', row.get(df.columns[1], '')))
                
                # Detect game type
                game_type = detect_game_type(row)
                
                # Extract draw ID
                draw_id = str(row.get('draw_info', ''))
                
                # Extract prizes
                prizes = extract_prizes(row)
                
                # Extract consolation and special numbers
                consolation_text = str(row.get('consolation', ''))
                special_text = str(row.get('special', ''))
                
                consolation_numbers = ' '.join(extract_4d_numbers(consolation_text))
                special_numbers = ' '.join(extract_4d_numbers(special_text))
                
                # Create normalized row
                normalized_row = {
                    'Date': date_val.strftime('%Y-%m-%d'),
                    'ProviderImageURL': str(row.get('provider', '')),
                    'GameType': game_type,
                    'DrawID': draw_id,
                    'DrawDetails': str(row.get('3rd', '')),
                    'Prize1': prizes['1st'],
                    'Prize2': prizes['2nd'],
                    'Prize3': prizes['3rd'],
                    'ConsolationNumbers': consolation_numbers,
                    'SpecialNumbers': special_numbers,
                    'Provider': provider
                }
                
                normalized_rows.append(normalized_row)
                
            except Exception as e:
                print(f"[WARN] Skipped row {idx}: {e}")
                continue
        
        # Create normalized DataFrame
        normalized_df = pd.DataFrame(normalized_rows)
        
        # Remove duplicates
        normalized_df = normalized_df.drop_duplicates(subset=['Date', 'Provider', 'Prize1'], keep='first')
        
        # Sort by date
        normalized_df = normalized_df.sort_values('Date')
        
        # Save to new file
        normalized_df.to_csv(output_file, index=False)
        
        print(f"\n[SUCCESS] Normalization complete!")
        print(f"[*] Original rows: {len(df)}")
        print(f"[*] Normalized rows: {len(normalized_df)}")
        print(f"[*] Saved to: {output_file}")
        print(f"\n[OK] Your original file '{input_file}' is UNTOUCHED and safe!")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    normalize_csv()
