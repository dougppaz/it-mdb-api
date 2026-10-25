import asyncio
import os

import pytest
import respx
from httpx import Response

import it_mdb_api.services.cache as cache_module
from it_mdb_api.services.cache import CacheService
from it_mdb_api.services.queue import QueueService
from it_mdb_api.worker import Worker


@pytest.fixture(autouse=True)
def reset_fake_server():
    os.environ["USE_FAKE_REDIS"] = "true"
    cache_module._shared_fake_server = None
    yield
    os.environ.pop("USE_FAKE_REDIS", None)


@pytest.mark.asyncio
@respx.mock
async def test_worker_processes_queue_item():
    respx.get("https://api.themoviedb.org/3/movie/550").mock(
        return_value=Response(
            200,
            json={
                "id": 550,
                "title": "Fight Club",
                "release_date": "1999-10-15",
                "vote_average": 8.4,
                "genres": [{"id": 18, "name": "Drama"}],
            },
        )
    )

    queue = QueueService()
    cache = CacheService()
    resource_key = "movie:tmdb:550:en-US"

    await queue.enqueue_task(
        "tasks:movies",
        {
            "tmdb_id": 550,
            "language": "en-US",
            "resource_key": resource_key,
        },
    )

    worker = Worker(queue_name="tasks:movies")

    async def run_one_task():
        for _ in range(20):
            cached = await cache.get(resource_key)
            if cached is not None:
                break
            await asyncio.sleep(0.05)
        worker.stop()

    worker_task = asyncio.create_task(worker.run())
    watcher_task = asyncio.create_task(run_one_task())

    await watcher_task
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

    cached_result = await cache.get(resource_key)
    assert cached_result is not None
    assert cached_result["title"] == "Fight Club"
    assert cached_result["year"] == 1999
