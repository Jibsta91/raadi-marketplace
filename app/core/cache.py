import json
import aioredis
from typing import Any, Optional
from datetime import timedelta
from app.core.config import settings


class CacheService:
    """Redis-based caching service for improved performance"""
    
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """Initialize Redis connection"""
        self.redis = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            await self.connect()
        
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: int = 3600
    ) -> bool:
        """Set value in cache with expiration"""
        if not self.redis:
            await self.connect()
        
        try:
            serialized_value = json.dumps(value, default=str)
            await self.redis.setex(key, expire, serialized_value)
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.redis:
            await self.connect()
        
        try:
            await self.redis.delete(key)
            return True
        except Exception:
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis:
            await self.connect()
        
        try:
            return bool(await self.redis.exists(key))
        except Exception:
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
