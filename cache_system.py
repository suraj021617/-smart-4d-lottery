"""
Simple in-memory caching system
Improves performance without external dependencies
"""
import time
from functools import wraps
import hashlib
import json

class SimpleCache:
    def __init__(self, ttl=300):
        self.cache = {}
        self.ttl = ttl  # Time to live in seconds
    
    def get(self, key):
        """Get cached value if not expired"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        """Set cache value with timestamp"""
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def delete(self, key):
        """Delete specific cache key"""
        if key in self.cache:
            del self.cache[key]

# Global cache instances
prediction_cache = SimpleCache(ttl=600)  # 10 minutes
data_cache = SimpleCache(ttl=300)  # 5 minutes

def cache_result(cache_name='default', ttl=300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{cache_name}:{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
            
            # Try to get from cache
            cached = prediction_cache.get(cache_key)
            if cached is not None:
                return cached
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            prediction_cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator
