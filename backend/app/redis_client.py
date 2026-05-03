import redis
import os
import json
from typing import Optional

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_cache(key: str) -> Optional[dict]:
    """Get cached data from Redis"""
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except Exception as e:
        print(f"Redis get error: {e}")
        return None

def set_cache(key: str, value: dict, ttl: int = 300):
    """Set cache in Redis with TTL (default 5 minutes)"""
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as e:
        print(f"Redis set error: {e}")

def delete_cache(key: str):
    """Delete cache from Redis"""
    try:
        redis_client.delete(key)
    except Exception as e:
        print(f"Redis delete error: {e}")
