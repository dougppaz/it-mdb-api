import asyncio
import os

import pytest

from it_mdb_api.services.cache import CacheService, get_redis_client
from it_mdb_api.services.queue import QueueService


@pytest.fixture(autouse=True)
def set_fake_redis():
    os.environ["USE_FAKE_REDIS"] = "true"
    yield
    os.environ.pop("USE_FAKE_REDIS", None)


@pytest.mark.asyncio
async def test_queue_enqueue_and_wait_cache_hit():
    client = get_redis_client()
    cache = CacheService(client)
    queue = QueueService(cache_service=cache, client=client)

    resource_key = "movie:imdb:tt123456:en"
    await cache.set(resource_key, {"title": "Test Movie"})

    result = await queue.enqueue_or_wait(
        resource_key=resource_key,
        queue_name="tasks:movies",
        task_payload={"id": "tt123456"},
        timeout=2,
    )
    assert result == {"title": "Test Movie"}


@pytest.mark.asyncio
async def test_queue_pubsub_notification():
    client = get_redis_client()
    cache = CacheService(client)
    queue = QueueService(cache_service=cache, client=client)

    resource_key = "movie:tmdb:550:en"
    queue_name = "tasks:movies"

    async def simulate_worker():
        await asyncio.sleep(0.2)
        await cache.set(resource_key, {"title": "Fight Club"})
        await queue.publish_ready(resource_key)

    worker_task = asyncio.create_task(simulate_worker())

    result = await queue.enqueue_or_wait(
        resource_key=resource_key,
        queue_name=queue_name,
        task_payload={"id": 550},
        timeout=3,
    )

    await worker_task
    assert result == {"title": "Fight Club"}


@pytest.mark.asyncio
async def test_queue_timeout():
    client = get_redis_client()
    cache = CacheService(client)
    queue = QueueService(cache_service=cache, client=client)

    resource_key = "movie:imdb:tt999999:en"

    with pytest.raises(TimeoutError):
        await queue.enqueue_or_wait(
            resource_key=resource_key,
            queue_name="tasks:movies",
            task_payload={"id": "tt999999"},
            timeout=1,
        )
