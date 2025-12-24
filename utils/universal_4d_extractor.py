"""Universal 4D Extractor - Logic from all working providers"""
import re
from datetime import datetime

def is_valid_4d(num):
    """Validate 4D: exactly 4 digits, 0000-9999"""
    return num and len(str(num)) == 4 and str(num).isdigit() and 0 <= int(num) <= 9999

def extract_4d_from_text(text):
    """Extract valid 4D numbers from any text"""
    numbers = re.findall(r'\b\d{4}\b', str(text))
    return [n for n in numbers if is_valid_4d(n)]

def extract_prizes(row_data):
    """Extract 1st, 2nd, 3rd prizes with multiple fallback methods"""
    text = str(row_data)
    
    # Method 1: Pattern matching (Da Ma Cai style)
    pattern1 = re.compile(r'1st.*?(\d{4}).*?2nd.*?(\d{4}).*?3rd.*?(\d{4})', re.IGNORECASE)
    match1 = pattern1.search(text)
    if match1:
        first, second, third = match1.groups()
        if all(is_valid_4d(n) for n in [first, second, third]):
            return first, second, third
    
    # Method 2: Column-based extraction (SportsToto style)
    if isinstance(row_data, dict):
        cols = ['1st_real', '2nd_real', '3rd_real', '1st', '2nd', '3rd', 'first', 'second', 'third']
        for prefix in ['', '_real', '_prize']:
            first = row_data.get(f'1st{prefix}') or row_data.get(f'first{prefix}')
            second = row_data.get(f'2nd{prefix}') or row_data.get(f'second{prefix}')
            third = row_data.get(f'3rd{prefix}') or row_data.get(f'third{prefix}')
            if all(is_valid_4d(n) for n in [first, second, third]):
                return str(first).zfill(4), str(second).zfill(4), str(third).zfill(4)
    
    # Method 3: Sequential extraction (Magnum style)
    all_4d = extract_4d_from_text(text)
    if len(all_4d) >= 3:
        return all_4d[0], all_4d[1], all_4d[2]
    
    return None, None, None

def extract_provider(row_data):
    """Extract provider name with normalization"""
    text = str(row_data).lower()
    providers = {
        'damacai': ['damacai', 'da ma cai', 'dmc'],
        'sportstoto': ['sportstoto', 'sports toto', 'toto'],
        'magnum': ['magnum', 'magnum4d'],
        'gdlotto': ['gdlotto', 'gd lotto', 'grand dragon'],
        'sabah': ['sabah', 'sabah88'],
        'stc': ['stc', 'sandakan']
    }
    
    for standard, aliases in providers.items():
        if any(alias in text for alias in aliases):
            return standard
    
    if isinstance(row_data, dict):
        return row_data.get('provider', 'Unknown')
    
    return 'Unknown'

def extract_date(row_data):
    """Extract and normalize date"""
    text = str(row_data)
    
    # Try multiple date formats
    patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # 2024-01-15
        r'(\d{2}/\d{2}/\d{4})',  # 15/01/2024
        r'(\d{2}-\d{2}-\d{4})',  # 15-01-2024
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            date_str = match.group(1)
            try:
                if '-' in date_str and len(date_str.split('-')[0]) == 4:
                    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                elif '/' in date_str:
                    return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                elif '-' in date_str:
                    return datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
            except:
                continue
    
    if isinstance(row_data, dict):
        return row_data.get('date') or row_data.get('draw_date', '')
    
    return ''

def clean_row(row_data):
    """Universal row cleaner using all provider logic"""
    first, second, third = extract_prizes(row_data)
    
    if not all([first, second, third]):
        return None
    
    return {
        'date': extract_date(row_data),
        'provider': extract_provider(row_data),
        '1st': first,
        '2nd': second,
        '3rd': third
    }
