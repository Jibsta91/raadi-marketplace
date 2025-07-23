import json
from typing import Any, Optional
from datetime import timedelta
from app.core.config import settings

# Simple fallback cache for testing
_fallback_cache = {}

class CacheService:
    """Redis-based caching service with fallback for testing"""
    
    def __init__(self):
        self.redis = None
        self.use_fallback = True
    
    async def connect(self):
        """Initialize Redis connection"""
        # For now, use fallback cache to avoid Redis dependency issues
        self.use_fallback = True
    
    async def disconnect(self):
        """Close Redis connection"""
        pass
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if self.use_fallback:
            return _fallback_cache.get(key)
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[timedelta] = None) -> bool:
        """Set value in cache"""
        if self.use_fallback:
            _fallback_cache[key] = value
            return True
        return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if self.use_fallback:
            _fallback_cache.pop(key, None)
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if self.use_fallback:
            return key in _fallback_cache
        return False
    
    async def clear(self) -> bool:
        """Clear all cache"""
        if self.use_fallback:
            _fallback_cache.clear()
            return True
        return False
    
    def generate_cache_key(self, prefix: str, *args) -> str:
        """Generate standardized cache key"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ":".join(key_parts)


# Global cache instance
cache = CacheService()


# Cache decorators for common use cases
def cache_result(expire: int = 3600, key_prefix: str = "result"):
    """Decorator to cache function results"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = cache.generate_cache_key(
                key_prefix, 
                func.__name__,
                str(args),
                str(sorted(kwargs.items()))
            )
            
            # Try to get cached result
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


def cache_listing(expire: int = 1800):
    """Decorator specifically for caching listing data"""
    return cache_result(expire=expire, key_prefix="listing")


def cache_user(expire: int = 3600):
    """Decorator specifically for caching user data"""
    return cache_result(expire=expire, key_prefix="user")


def cache_search(expire: int = 600):
    """Decorator specifically for caching search results"""
    return cache_result(expire=expire, key_prefix="search")
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key based on function name and arguments
            cache_key = cache.generate_cache_key(
                key_prefix,
                func.__name__,
                *args,
                *[f"{k}:{v}" for k, v in sorted(kwargs.items())]
            )
            
            # Try to get from cache first
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, expire)
            return result
        
        return wrapper
    return decorator


async def cache_listings(category: str = None, location: str = None):
    """Cache popular listings by category and location"""
    cache_key = cache.generate_cache_key("listings", category or "all", location or "all")
    return await cache.get(cache_key)


async def invalidate_listings_cache():
    """Invalidate all listings cache when new listing is created"""
    # This would require pattern matching in Redis
    # For now, we'll use a simple approach
    keys_to_delete = [
        "listings:*",
        "search:*",
        "categories:*"
    ]
    for pattern in keys_to_delete:
        try:
            if cache.redis:
                keys = await cache.redis.keys(pattern)
                if keys:
                    await cache.redis.delete(*keys)
        except Exception:
            pass
