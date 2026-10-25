import asyncio
import os

import pytest
from httpx import ASGITransport, AsyncClient

import it_mdb_api.services.cache as cache_module
from it_mdb_api.main import app
from it_mdb_api.services.cache import CacheService
from it_mdb_api.services.queue import QueueService


@pytest.fixture(autouse=True)
def reset_fake_server():
    os.environ["USE_FAKE_REDIS"] = "true"
    cache_module._shared_fake_server = None
    yield
    os.environ.pop("USE_FAKE_REDIS", None)


@pytest.mark.asyncio
async def test_get_tmdb_movie_cache_hit():
    cache = CacheService()
    resource_key = "movie:tmdb:550:en-US"
    await cache.set(resource_key, {"id": "550", "title": "Fight Club"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/550")

    assert response.status_code == 200
    assert response.json() == {"id": "550", "title": "Fight Club"}


@pytest.mark.asyncio
async def test_get_tmdb_movie_queue_wait_and_populate():
    cache = CacheService()
    queue = QueueService()
    resource_key = "movie:tmdb:550:en-US"

    async def simulate_worker():
        await asyncio.sleep(0.2)
        await cache.set(resource_key, {"id": "550", "title": "Fight Club (Worker)"})
        await queue.publish_ready(resource_key)

    worker_task = asyncio.create_task(simulate_worker())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/550?timeout=3")

    await worker_task
    assert response.status_code == 200
    assert response.json() == {"id": "550", "title": "Fight Club (Worker)"}


@pytest.mark.asyncio
async def test_get_tmdb_movie_timeout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/999?timeout=1")

    assert response.status_code == 504
