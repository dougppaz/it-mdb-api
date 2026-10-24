import asyncio
import json
import logging
from typing import Any

import redis.asyncio as redis

from it_mdb_api.services.cache import CacheService

logger = logging.getLogger(__name__)


class QueueService:
    def __init__(
        self,
        cache_service: CacheService | None = None,
        client: redis.Redis | None = None,
    ):
        self.cache_service = cache_service or CacheService(client=client)
        self.client = self.cache_service.client

    async def enqueue_or_wait(
        self,
        resource_key: str,
        queue_name: str,
        task_payload: dict,
        timeout: int = 30,
        poll_interval: float = 0.5,
    ) -> Any:
        """1. Check cache. If hit, return data.

        2. Check if task is already queued/processing via atomic dedup key. 3.
        If not, push to queue. 4. Wait for cache readiness via PubSub / polling
        up to timeout.
        """
        # Step 1: Check cache
        cached = await self.cache_service.get(resource_key)
        if cached is not None:
            return cached

        # Step 2 & 3: Deduplication and queue push
        dedup_key = f"dedup:{resource_key}"
        is_new_task = await self.cache_service.set_nx(
            dedup_key, "processing", ttl=max(timeout * 2, 60)
        )

        if is_new_task:
            await self.client.rpush(queue_name, json.dumps(task_payload))
            logger.info("Enqueued task for %s to %s", resource_key, queue_name)
        else:
            logger.info(
                "Task for %s already queued/processing, listening for result",
                resource_key,
            )

        # Step 4: Wait for cache readiness (PubSub + Polling fallback)
        channel_name = f"channel:{resource_key}"
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel_name)

        loop = asyncio.get_running_loop()
        end_time = loop.time() + timeout

        try:
            while loop.time() < end_time:
                cached = await self.cache_service.get(resource_key)
                if cached is not None:
                    return cached

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
                        cached = await self.cache_service.get(resource_key)
                        if cached is not None:
                            return cached
                except TimeoutError:
                    pass
        finally:
            await pubsub.unsubscribe(channel_name)
            await pubsub.aclose()

        cached = await self.cache_service.get(resource_key)
        if cached is not None:
            return cached

        raise TimeoutError(
            f"Timed out waiting for resource {resource_key} after {timeout} seconds"
        )

    async def publish_ready(self, resource_key: str) -> None:
        """Notifies all waiting requests that the resource is now cached."""
        channel_name = f"channel:{resource_key}"
        await self.client.publish(channel_name, "ready")
