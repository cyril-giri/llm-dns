from cachetools import TTLCache
from typing import Optional

# Global cache instance
cache = TTLCache(maxsize=1000, ttl=300)

def get_cached_response(prompt: str) -> Optional[str]:
    """Get cached response if available."""
    return cache.get(prompt)

def cache_response(prompt: str, response: str) -> None:
    """Cache a response for future use."""
    cache[prompt] = response