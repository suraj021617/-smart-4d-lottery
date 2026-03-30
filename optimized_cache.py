"""
Optimized Cache System for Smart 4D Lottery Prediction
- Smart TTL (Time To Live) based on data freshness
- LRU (Least Recently Used) eviction
- Thread-safe operations
- Memory-efficient
"""
import time
import threading
from collections import OrderedDict
from datetime import datetime, timedelta

class SmartCache:
    def __init__(self, max_size=50, ttl_seconds=3600):
        self.cache = OrderedDict()
        self.timestamps = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.lock = threading.Lock()
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            # Check TTL
            if time.time() - self.timestamps[key] > self.ttl_seconds:
                del self.cache[key]
                del self.timestamps[key]
                self.misses += 1
                return None
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
    
    def set(self, key, value):
        with self.lock:
            # Remove oldest if at capacity
            if len(self.cache) >= self.max_size and key not in self.cache:
                oldest = next(iter(self.cache))
                del self.cache[oldest]
                del self.timestamps[oldest]
            
            self.cache[key] = value
            self.timestamps[key] = time.time()
            self.cache.move_to_end(key)
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': round(hit_rate, 1),
            'size': len(self.cache)
        }

# Global cache instances
_smart_cache = SmartCache(max_size=30, ttl_seconds=1800)  # 30 min TTL
_ml_cache = SmartCache(max_size=20, ttl_seconds=3600)     # 1 hour TTL
_data_cache = SmartCache(max_size=5, ttl_seconds=300)     # 5 min TTL

def get_cache_stats():
    return {
        'smart_predictor': _smart_cache.stats(),
        'ml_predictor': _ml_cache.stats(),
        'data_loader': _data_cache.stats()
    }
