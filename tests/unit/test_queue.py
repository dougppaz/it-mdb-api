import asyncio
import os

import pytest

from it_mdb_api.services.queue import QueueService, get_queue_redis_client


@pytest.fixture(autouse=True)
def set_fake_redis():
    os.environ["USE_FAKE_REDIS"] = "true"
    yield
    os.environ.pop("USE_FAKE_REDIS", None)


@pytest.mark.asyncio
async def test_queue_dedup_lock():
    client = get_queue_redis_client()
    queue = QueueService(client=client)

    resource_key = "movie:imdb:tt123456:en"
    locked1 = await queue.acquire_dedup_lock(resource_key, ttl=10)
    assert locked1 is True

    locked2 = await queue.acquire_dedup_lock(resource_key, ttl=10)
    assert locked2 is False


@pytest.mark.asyncio
async def test_queue_pubsub_wait_and_publish():
    client = get_queue_redis_client()
    queue = QueueService(client=client)

    resource_key = "movie:tmdb:550:en"

    async def simulate_worker():
        await asyncio.sleep(0.2)
        await queue.publish_ready(resource_key)

    worker_task = asyncio.create_task(simulate_worker())

    notified = await queue.wait_for_readiness(resource_key, timeout=3)
    await worker_task

    assert notified is True


@pytest.mark.asyncio
async def test_queue_wait_timeout():
    client = get_queue_redis_client()
    queue = QueueService(client=client)

    resource_key = "movie:imdb:tt999999:en"
    notified = await queue.wait_for_readiness(resource_key, timeout=1)
    assert notified is False
