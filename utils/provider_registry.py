"""
Provider Registry - Single Source of Truth for Provider Normalization
Prevents provider name inconsistencies across the entire application
"""

class ProviderRegistry:
    """Canonical provider definitions and normalization rules"""
    
    # Canonical provider keys (lowercase, no spaces)
    PROVIDERS = {
        'sportstoto': {
            'display_name': 'Sports Toto',
            'aliases': ['sports toto', 'sportstoto', 'toto', 'sports-toto', 'sport toto'],
            'color': '#FF6B6B',
            'logo': 'toto.png'
        },
        'magnum': {
            'display_name': 'Magnum 4D',
            'aliases': ['magnum', 'magnum4d', 'magnum 4d'],
            'color': '#4ECDC4',
            'logo': 'magnum.png'
        },
        'damacai': {
            'display_name': 'Da Ma Cai',
            'aliases': ['damacai', 'da ma cai', 'dmc', 'da-ma-cai'],
            'color': '#FFE66D',
            'logo': 'damacai.png'
        },
        'gdlotto': {
            'display_name': 'GD Lotto',
            'aliases': ['gdlotto', 'gd lotto', 'grand dragon', 'gd'],
            'color': '#95E1D3',
            'logo': 'gdlotto.png'
        },
        'perdana': {
            'display_name': 'Perdana 4D',
            'aliases': ['perdana', 'perdana4d'],
            'color': '#F38181',
            'logo': 'perdana.png'
        },
        'sabah': {
            'display_name': 'Sabah 88',
            'aliases': ['sabah', 'sabah88', 'sabah 88'],
            'color': '#AA96DA',
            'logo': 'sabah.png'
        },
        'stc': {
            'display_name': 'STC 4D',
            'aliases': ['stc', 'stc4d', 'sandakan'],
            'color': '#FCBAD3',
            'logo': 'stc.png'
        }
    }
    
    @classmethod
    def normalize(cls, raw_provider):
        """
        Normalize any provider string to canonical key
        
        Args:
            raw_provider: Raw provider string from CSV/user input
            
        Returns:
            Canonical provider key (e.g., 'sportstoto')
        """
        if not raw_provider:
            return 'unknown'
        
        # Clean input
        cleaned = str(raw_provider).lower().strip()
        
        # Direct match
        if cleaned in cls.PROVIDERS:
            return cleaned
        
        # Alias matching
        for canonical_key, config in cls.PROVIDERS.items():
            if cleaned in config['aliases']:
                return canonical_key
        
        return 'unknown'
    
    @classmethod
    def get_display_name(cls, canonical_key):
        """Get user-friendly display name"""
        return cls.PROVIDERS.get(canonical_key, {}).get('display_name', canonical_key.upper())
    
    @classmethod
    def get_all_canonical_keys(cls):
        """Get list of all canonical provider keys"""
        return list(cls.PROVIDERS.keys())
    
    @classmethod
    def get_provider_config(cls, canonical_key):
        """Get full provider configuration"""
        return cls.PROVIDERS.get(canonical_key, {})
