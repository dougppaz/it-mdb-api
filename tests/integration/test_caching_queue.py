import asyncio
import os

import pytest
import respx
from httpx import ASGITransport, AsyncClient, Response

import it_mdb_api.services.cache as cache_module
from it_mdb_api.main import app
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
async def test_e2e_concurrent_requests_and_deduplication():
    respx.get("https://api.themoviedb.org/3/movie/299534").mock(
        return_value=Response(
            200,
            json={
                "id": 299534,
                "title": "Avengers: Endgame",
                "release_date": "2019-04-24",
                "vote_average": 8.3,
                "genres": [{"id": 12, "name": "Adventure"}],
            },
        )
    )

    queue = QueueService()

    worker = Worker(queue_name="tasks:movies")
    worker_task = asyncio.create_task(worker.run())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        responses = await asyncio.gather(
            ac.get("/v1/movies/299534?timeout=5"),
            ac.get("/v1/movies/299534?timeout=5"),
            ac.get("/v1/movies/299534?timeout=5"),
        )

    worker.stop()
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

    for response in responses:
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "299534"
        assert data["title"] == "Avengers: Endgame"

    queue_len = await queue.client.llen("tasks:movies")
    assert queue_len == 0
