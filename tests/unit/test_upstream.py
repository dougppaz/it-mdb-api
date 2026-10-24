import pytest
import respx
from httpx import Response

from it_mdb_api.services.upstream import UpstreamClient


@pytest.mark.asyncio
@respx.mock
async def test_fetch_tmdb_movie_success():
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

    client = UpstreamClient()
    movie = await client.fetch_tmdb_movie(550, language="en-US")

    assert movie["id"] == "550"
    assert movie["title"] == "Fight Club"
    assert movie["year"] == 1999
    assert movie["rating"] == 8.4
    assert movie["genres"] == ["Drama"]


@pytest.mark.asyncio
@respx.mock
async def test_fetch_tmdb_movie_not_found():
    respx.get("https://api.themoviedb.org/3/movie/999999").mock(
        return_value=Response(
            404,
            json={
                "status_message": "The resource you requested could not be found."
            },
        )
    )

    client = UpstreamClient()
    with pytest.raises(LookupError):
        await client.fetch_tmdb_movie(999999)
