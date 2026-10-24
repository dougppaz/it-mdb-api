import json
import os
from typing import Any

import redis.asyncio as redis


def get_redis_client() -> redis.Redis:
    if os.getenv("USE_FAKE_REDIS", "").lower() in ("true", "1", "yes"):
        from fakeredis import aioredis as fake_redis

        return fake_redis.FakeRedis(decode_responses=True)
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(redis_url, decode_responses=True)


class CacheService:
    def __init__(self, client: redis.Redis | None = None):
        self.client = client or get_redis_client()

    async def get(self, key: str) -> Any | None:
        val = await self.client.get(key)
        if val is None:
            return None
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return val

    async def set(self, key: str, value: Any, ttl: int = 86400) -> None:
        serialized = json.dumps(value) if not isinstance(value, str) else value
        await self.client.set(key, serialized, ex=ttl)

    async def set_nx(self, key: str, value: str, ttl: int) -> bool:
        res = await self.client.set(key, value, ex=ttl, nx=True)
        return bool(res)
