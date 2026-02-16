import hashlib
import json
from functools import wraps
from typing import Optional

# Simple in-memory cache (upgrade to Redis when available)
_cache: dict[str, tuple[float, any]] = {}


def cache_response(ttl_seconds: int = 300, key_prefix: str = ""):
    """Decorator to cache endpoint responses in memory."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import time
            # Build cache key from function name + args
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(json.dumps(str(kwargs), sort_keys=True).encode()).hexdigest()}"

            # Check cache
            if cache_key in _cache:
                cached_time, cached_value = _cache[cache_key]
                if time.time() - cached_time < ttl_seconds:
                    return cached_value

            # Execute and cache
            result = await func(*args, **kwargs)
            _cache[cache_key] = (time.time(), result)
            return result
        return wrapper
    return decorator


def clear_cache(prefix: str = ""):
    """Clear cache entries matching prefix."""
    if not prefix:
        _cache.clear()
    else:
        keys_to_delete = [k for k in _cache if k.startswith(prefix)]
        for k in keys_to_delete:
            del _cache[k]
