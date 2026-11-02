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
async def test_get_imdb_movie_cache_hit():
    cache = CacheService()
    resource_key = "movie:imdb:tt0137523:en"
    await cache.set(
        resource_key, {"id": "550", "title": "Fight Club", "imdb_id": "tt0137523"}
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/tt0137523")

    assert response.status_code == 200
    assert response.json() == {
        "id": "550",
        "title": "Fight Club",
        "imdb_id": "tt0137523",
    }


@pytest.mark.asyncio
async def test_get_imdb_movie_timeout():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/tt9999999?timeout=1")

    assert response.status_code == 504


@pytest.mark.asyncio
async def test_get_tmdb_tvshow_cache_hit():
    cache = CacheService()
    resource_key = "tvshow:tmdb:1399:en-US"
    await cache.set(resource_key, {"id": "1399", "title": "Game of Thrones"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/tvshows/1399")

    assert response.status_code == 200
    assert response.json() == {"id": "1399", "title": "Game of Thrones"}


@pytest.mark.asyncio
async def test_get_imdb_tvshow_cache_hit():
    cache = CacheService()
    resource_key = "tvshow:imdb:tt0944947:en"
    await cache.set(
        resource_key, {"id": "1399", "title": "Game of Thrones", "imdb_id": "tt0944947"}
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/tvshows/tt0944947")

    assert response.status_code == 200
    assert response.json() == {
        "id": "1399",
        "title": "Game of Thrones",
        "imdb_id": "tt0944947",
    }


@pytest.mark.asyncio
async def test_openapi_schemas():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/openapi.json")

    assert response.status_code == 200
    openapi_spec = response.json()
    schemas = openapi_spec.get("components", {}).get("schemas", {})
    assert "MovieV1" in schemas
    assert "TVShowV1" in schemas

    paths = openapi_spec.get("paths", {})
    for path_key in [
        "/v1/movies/{tmdb_id}",
        "/v1/movies/tt{imdb_id}",
        "/v1/tvshows/{tmdb_id}",
        "/v1/tvshows/tt{imdb_id}",
    ]:
        path_item = paths.get(path_key, {})
        assert path_item, f"Path {path_key} missing in openapi"
        # Check get operation responses
        get_op = path_item.get("get", {})
        responses = get_op.get("responses", {})
        assert "404" in responses, f"404 response missing in openapi for {path_key}"
        assert "504" in responses, f"504 response missing in openapi for {path_key}"


@pytest.mark.asyncio
async def test_get_movie_not_found_cached():
    cache = CacheService()
    resource_key = "movie:imdb:tt39300469:pt-BR"
    await cache.set(resource_key, {"error": "Not found"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/movies/tt39300469?language=pt-BR")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}


@pytest.mark.asyncio
async def test_get_tvshow_not_found_cached():
    cache = CacheService()
    resource_key = "tvshow:tmdb:999999:en-US"
    await cache.set(resource_key, {"error": "Not found"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/v1/tvshows/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
