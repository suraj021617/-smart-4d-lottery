"""
Fix provider filtering logic across all routes
Run this to patch app.py with correct provider filtering
"""

import re

def fix_provider_filtering():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Fix pattern-analyzer route
    pattern1 = r"    # Filter by provider - exact match\n    if selected_provider and selected_provider != 'all':\n        month_draws = month_draws\[month_draws\['provider_key'\] == selected_provider\]"
    
    replacement1 = """    # Filter by provider - normalized match
    if selected_provider and selected_provider != 'all':
        from utils.data_normalizer import DataNormalizer
        normalized_provider = DataNormalizer.normalize_provider(selected_provider)
        month_draws = month_draws[month_draws['provider_key'] == normalized_provider]"""
    
    content = re.sub(pattern1, replacement1, content)
    
    # Pattern 2: Fix all other provider filters
    pattern2 = r"    if provider != 'all':\n        df = df\[df\['provider_key'\] == provider\]"
    
    replacement2 = """    if provider != 'all':
        from utils.data_normalizer import DataNormalizer
        normalized_provider = DataNormalizer.normalize_provider(provider)
        df = df[df['provider_key'] == normalized_provider]"""
    
    content = re.sub(pattern2, replacement2, content)
    
    # Pattern 3: Fix selected_provider filters
    pattern3 = r"    if selected_provider != 'all':\n        df = df\[df\['provider_key'\] == selected_provider\]"
    
    replacement3 = """    if selected_provider != 'all':
        from utils.data_normalizer import DataNormalizer
        normalized_provider = DataNormalizer.normalize_provider(selected_provider)
        df = df[df['provider_key'] == normalized_provider]"""
    
    content = re.sub(pattern3, replacement3, content)
    
    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("[OK] Fixed provider filtering logic in app.py")
    print("Provider filters now use normalized provider keys")

if __name__ == '__main__':
    fix_provider_filtering()
