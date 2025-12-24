"""
Canonical Data Normalization Layer
Single source of truth for all data cleaning and validation
"""
import re
import pandas as pd
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Universal data normalizer for 4D lottery data"""
    
    @staticmethod
    def normalize_provider(raw_provider: str) -> str:
        """
        Normalize provider name to canonical key
        Handles both URLs and plain text provider names
        """
        if pd.isna(raw_provider) or not raw_provider:
            return "unknown"
        
        # Convert to string and lowercase
        normalized = str(raw_provider).lower().strip()
        
        # Extract provider from URL path (e.g., /images/singapore -> singapore)
        url_match = re.search(r'/images/([a-z0-9]+)', normalized)
        if url_match:
            normalized = url_match.group(1)
        else:
            # Remove URLs and domains if present
            normalized = re.sub(r'https?://', '', normalized)
            normalized = re.sub(r'www\.', '', normalized)
            normalized = re.sub(r'live4d2u\.net/?', '', normalized)
            normalized = re.sub(r'/images/', '', normalized)
            # Keep only alphanumeric characters
            normalized = re.sub(r'[^a-z0-9]', '', normalized)
        
        # Map URL paths to display names (EXACT mapping)
        provider_map = {
            'toto': 'Sports Toto',
            'sportstoto': 'Sports Toto',
            'stc': 'Sports Toto',
            'stc4d': 'Sports Toto',
            'damacai': 'Da Ma Cai',
            'dmc': 'Da Ma Cai',
            'pmp': 'Da Ma Cai',
            'magnum': 'Magnum 4D',
            'magnum4d': 'Magnum 4D',
            'magnumlife': 'Magnum 4D',
            'jackpotgold': 'Magnum 4D',
            'gdlotto': 'GD Lotto',
            'gd': 'GD Lotto',
            'granddragon4d': 'GD Lotto',
            'granddragon': 'GD Lotto',
            'sabah88': 'Sabah 88 4D',
            'sabah884d': 'Sabah 88 4D',
            'sabah88lotto': 'Sabah 88 Lotto',
            'sandakan': 'Sandakan 4D',
            'sandakan4d': 'Sandakan 4D',
            'cashsweep': 'Cash Sweep 4D',
            'cashsweep4d': 'Cash Sweep 4D',
            'singapore': 'Singapore 4D',
            'singapore4d': 'Singapore 4D',
            'perdana': 'Perdana',
            'perdanalottery4d': 'Perdana',
            'harihari': 'Hari Hari',
            'luckyharihari4d': 'Hari Hari',
            'luckyharihari': 'Hari Hari'
        }
        
        return provider_map.get(normalized, normalized.title())
    
    @staticmethod
    def normalize_4d_number(raw_number: Any) -> Optional[str]:
        """
        Normalize 4D number to zero-padded 4-digit string
        
        Examples:
            123 -> "0123"
            "1234" -> "1234"
            "12 34" -> "1234"
            "abc" -> None (invalid)
        """
        if pd.isna(raw_number):
            return None
        
        # Convert to string and remove all whitespace
        num_str = str(raw_number).strip().replace(' ', '')
        
        # Keep only digits
        digits_only = re.sub(r'\D', '', num_str)
        
        # Validate length
        if not digits_only or len(digits_only) > 4:
            return None
        
        # Zero-pad to 4 digits
        normalized = digits_only.zfill(4)
        
        # Validate range (0000-9999)
        if 0 <= int(normalized) <= 9999:
            return normalized
        
        return None
    
    @staticmethod
    def normalize_date(raw_date: Any) -> Optional[pd.Timestamp]:
        """
        Normalize date to pandas Timestamp
        
        Handles multiple formats:
            "2024-01-15"
            "15/01/2024"
            "Jan 15, 2024"
        """
        if pd.isna(raw_date):
            return None
        
        try:
            return pd.to_datetime(raw_date, errors='coerce')
        except:
            return None
    
    @staticmethod
    def extract_numbers_from_text(text: str) -> Dict[str, Optional[str]]:
        """
        Extract ALL 4D numbers from scraped text
        
        Example text:
            "1st Prize 4529 | 2nd Prize 7748 | 3rd Prize 8891"
            "6644 8554 2372 1862 2884 5408"
        
        Returns:
            {'1st': '4529', '2nd': '7748', '3rd': '8891', 'all': ['4529', '7748', '8891', ...]}
        """
        result = {'1st': None, '2nd': None, '3rd': None, 'all': []}
        
        if pd.isna(text) or not text:
            return result
        
        text = str(text)
        
        # Extract ALL 4-digit numbers from text
        all_4d = re.findall(r'\b\d{4}\b', text)
        result['all'] = [DataNormalizer.normalize_4d_number(n) for n in all_4d if DataNormalizer.normalize_4d_number(n)]
        
        # Try to identify 1st, 2nd, 3rd prizes if labeled
        first_match = re.search(r'1st[^0-9]*(\d{4})(?!\d)', text, re.IGNORECASE)
        if first_match:
            result['1st'] = DataNormalizer.normalize_4d_number(first_match.group(1))
        
        second_match = re.search(r'2nd[^0-9]*(\d{4})(?!\d)', text, re.IGNORECASE)
        if second_match:
            result['2nd'] = DataNormalizer.normalize_4d_number(second_match.group(1))
        
        third_match = re.search(r'3rd[^0-9]*(\d{4})(?!\d)', text, re.IGNORECASE)
        if third_match:
            result['3rd'] = DataNormalizer.normalize_4d_number(third_match.group(1))
        
        # If no labeled prizes, use first 3 numbers found
        if not result['1st'] and len(result['all']) >= 1:
            result['1st'] = result['all'][0]
        if not result['2nd'] and len(result['all']) >= 2:
            result['2nd'] = result['all'][1]
        if not result['3rd'] and len(result['all']) >= 3:
            result['3rd'] = result['all'][2]
        
        return result
    
    @staticmethod
    def validate_row(row: pd.Series) -> bool:
        """
        Validate if row has minimum required data
        
        Returns True if row has:
        - Valid date
        - Valid provider
        - At least one valid 4D number
        """
        has_date = pd.notna(row.get('date_parsed'))
        has_provider = row.get('provider_key') not in [None, '', 'unknown']
        has_number = any([
            row.get('number_1st'),
            row.get('number_2nd'),
            row.get('number_3rd')
        ])
        
        return has_date and has_provider and has_number


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse CSV by EXACT column positions - no guessing
    """
    df = df.copy()
    
    # Column positions (0-indexed)
    # 0: date
    # 1: provider (URL)
    # 2: draw_info (provider name)
    # 3: draw_number
    # 4: draw_date_text
    # 5: prize_text (contains 1st/2nd/3rd)
    # 6: special
    # 7: consolation
    
    # Parse date from column 0
    df['date_parsed'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
    
    # Get provider from column 1 (URL) - this is the TRUE provider
    df['provider_key'] = df.iloc[:, 1].apply(DataNormalizer.normalize_provider)
    
    # 🎯 FILTER: Skip non-4D lottery types (5D, 6D, Lotto, etc.)
    df['lottery_type'] = df.iloc[:, 2].astype(str).str.lower()
    non_4d_keywords = ['5d', '6d', 'lotto', 'magnum life', 'jackpot gold', 'singapore toto', 'sabah 88 lotto', '3+3d', '1+3d']
    df['is_4d_only'] = ~df['lottery_type'].str.contains('|'.join(non_4d_keywords), case=False, na=False)
    df = df[df['is_4d_only']].copy()
    logger.info(f"Filtered to 4D-only: {len(df)} rows (excluded 5D/6D/Lotto)")
    
    # Extract numbers
    extracted_data = []
    
    for idx, row in df.iterrows():
        # Column 5: prize_text (1st/2nd/3rd prizes)
        prize_text = str(row.iloc[5]) if len(row) > 5 else ''
        # Column 6: special
        special_text = str(row.iloc[6]) if len(row) > 6 else ''
        # Column 7: consolation
        consolation_text = str(row.iloc[7]) if len(row) > 7 else ''
        
        # Extract 1st, 2nd, 3rd from prize_text
        first = re.search(r'1st[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        second = re.search(r'2nd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        third = re.search(r'3rd[^0-9]*(\d{4})', prize_text, re.IGNORECASE)
        
        first_num = first.group(1) if first else None
        second_num = second.group(1) if second else None
        third_num = third.group(1) if third else None
        
        # Extract special (all 4D numbers)
        special_4d = re.findall(r'\b\d{4}\b', special_text)
        special_nums = [n for n in special_4d if n != '----' and n != '****'][:10]
        
        # Extract consolation (all 4D numbers)
        consolation_4d = re.findall(r'\b\d{4}\b', consolation_text)
        consolation_nums = [n for n in consolation_4d if n != '----' and n != '****'][:10]
        
        extracted_data.append({
            'number_1st': first_num,
            'number_2nd': second_num,
            'number_3rd': third_num,
            'special': ' '.join(special_nums) if special_nums else '',
            'consolation': ' '.join(consolation_nums) if consolation_nums else '',
            'total_4d_found': len([n for n in [first_num, second_num, third_num] if n]) + len(special_nums) + len(consolation_nums)
        })
    
    # Add extracted columns
    for key in ['number_1st', 'number_2nd', 'number_3rd', 'special', 'consolation', 'total_4d_found']:
        df[key] = [d[key] for d in extracted_data]
    
    # Validate: must have date + provider + at least one 4D number
    df['is_valid'] = (
        df['date_parsed'].notna() & 
        (df['provider_key'] != 'unknown') &
        (df['number_1st'].notna() | df['number_2nd'].notna() | df['number_3rd'].notna())
    )
    
    valid_count = df['is_valid'].sum()
    logger.info(f"Extracted: {valid_count}/{len(df)} valid rows, Total 4D: {df['total_4d_found'].sum()}")
    
    return df
