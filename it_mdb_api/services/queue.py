import asyncio
import json
import logging

import redis.asyncio as redis

from it_mdb_api.services.cache import get_shared_fake_server
from it_mdb_api.settings import RedisSettings

logger = logging.getLogger(__name__)


def get_queue_redis_client() -> redis.Redis:
    redis_settings = RedisSettings()
    if redis_settings.use_fake_redis:
        from fakeredis import aioredis as fake_redis

        return fake_redis.FakeRedis(
            server=get_shared_fake_server(), db=0, decode_responses=True
        )
    url = redis_settings.queue_redis_url or redis_settings.redis_url
    return redis.from_url(url, decode_responses=True)


class QueueService:
    def __init__(self, client: redis.Redis | None = None):
        self.client = client or get_queue_redis_client()

    async def acquire_dedup_lock(self, resource_key: str, ttl: int = 60) -> bool:
        """Acquires an atomic deduplication lock for the resource."""
        dedup_key = f"dedup:{resource_key}"
        res = await self.client.set(dedup_key, "processing", ex=ttl, nx=True)
        return bool(res)

    async def enqueue_task(self, queue_name: str, task_payload: dict) -> None:
        """Pushes a task payload to the Redis queue."""
        await self.client.rpush(queue_name, json.dumps(task_payload))
        logger.info("Enqueued task to %s", queue_name)

    async def wait_for_readiness(
        self,
        resource_key: str,
        timeout: int = 30,
        poll_interval: float = 0.5,
    ) -> bool:
        """Subscribes to Redis PubSub channel for the resource and waits for

        notification or timeout. Returns True if notified/ready, False if
        timed out.
        """
        channel_name = f"channel:{resource_key}"
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel_name)

        loop = asyncio.get_running_loop()
        end_time = loop.time() + timeout

        try:
            while loop.time() < end_time:
                remaining = end_time - loop.time()
                if remaining <= 0:
                    break

                try:
                    message = await asyncio.wait_for(
                        pubsub.get_message(
                            ignore_subscribe_messages=True,
                            timeout=min(poll_interval, remaining),
                        ),
                        timeout=min(poll_interval + 0.1, remaining),
                    )
                    if message and message.get("type") == "message":
                        return True
                except TimeoutError:
                    pass
        finally:
            await pubsub.unsubscribe(channel_name)
            await pubsub.aclose()

        return False

    async def publish_ready(self, resource_key: str) -> None:
        """Publishes readiness notification to the resource channel."""
        channel_name = f"channel:{resource_key}"
        await self.client.publish(channel_name, "ready")
