"""
Security Fixes for Smart 4D Lottery System
- Safe input validation
- SQL injection prevention
- XSS protection
- Safe data parsing
"""
import re
import json
from typing import List, Optional

def validate_4d_number(number: str) -> bool:
    """Validate 4D number format"""
    if not isinstance(number, str):
        return False
    return bool(re.match(r'^\d{4}$', number))

def sanitize_provider(provider: str) -> str:
    """Sanitize provider name"""
    if not provider:
        return 'all'
    # Remove special characters, keep alphanumeric and spaces
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', str(provider))
    return clean.strip().lower()[:50]  # Max 50 chars

def safe_parse_predictions(predictions_str: str) -> List[str]:
    """Safely parse prediction numbers from string"""
    if not predictions_str or not isinstance(predictions_str, str):
        return []
    
    # Try JSON first
    if predictions_str.startswith('['):
        try:
            parsed = json.loads(predictions_str)
            if isinstance(parsed, list):
                return [str(n) for n in parsed if validate_4d_number(str(n))]
        except (json.JSONDecodeError, ValueError):
            pass
    
    # Fallback to regex extraction
    numbers = re.findall(r'\b\d{4}\b', predictions_str)
    return [n for n in numbers if validate_4d_number(n)][:10]  # Max 10 numbers

def validate_date(date_str: str) -> Optional[str]:
    """Validate and sanitize date string"""
    if not date_str:
        return None
    
    # Extract YYYY-MM-DD format
    match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', str(date_str))
    if match:
        year, month, day = match.groups()
        # Basic validation
        if 2020 <= int(year) <= 2030 and 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
            return f"{year}-{month}-{day}"
    return None

def sanitize_sql_input(value: str) -> str:
    """Prevent SQL injection"""
    if not value:
        return ''
    # Remove SQL keywords and special chars
    dangerous = ['--', ';', '/*', '*/', 'xp_', 'sp_', 'DROP', 'DELETE', 'INSERT', 'UPDATE']
    clean = str(value)
    for keyword in dangerous:
        clean = clean.replace(keyword, '')
    return clean[:200]  # Max length

def validate_confidence(confidence) -> float:
    """Validate confidence score"""
    try:
        val = float(confidence)
        return max(0.0, min(100.0, val))  # Clamp to 0-100
    except (ValueError, TypeError):
        return 50.0  # Default

# XSS Protection
def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    if not text:
        return ''
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#x27;'))
