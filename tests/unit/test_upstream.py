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
                "poster_path": "/poster.jpg",
                "backdrop_path": "/backdrop.jpg",
            },
        )
    )
    respx.get("https://api.themoviedb.org/3/movie/550/external_ids").mock(
        return_value=Response(
            200,
            json={
                "id": 550,
                "imdb_id": "tt0137523",
            },
        )
    )

    client = UpstreamClient()
    movie = await client.fetch_tmdb_movie(550, language="en-US")

    assert movie["id"] == "550"
    assert movie["title"] == "Fight Club"
    assert movie["year"] == 1999
    assert movie["tmdb_poster_path"] == "/poster.jpg"
    assert movie["tmdb_backdrop_path"] == "/backdrop.jpg"
    assert movie["imdb_id"] == "tt0137523"
    assert movie["tmdb_id"] == 550


@pytest.mark.asyncio
@respx.mock
async def test_fetch_imdb_movie_success():
    respx.get("https://api.themoviedb.org/3/find/tt0137523").mock(
        return_value=Response(
            200,
            json={
                "movie_results": [
                    {
                        "id": 550,
                        "title": "Fight Club",
                        "release_date": "1999-10-15",
                        "poster_path": "/poster.jpg",
                        "backdrop_path": "/backdrop.jpg",
                        "imdb_id": "tt0137523",
                    }
                ]
            },
        )
    )

    client = UpstreamClient()
    movie = await client.fetch_imdb_movie("tt0137523", language="en")

    assert movie["id"] == "550"
    assert movie["title"] == "Fight Club"
    assert movie["year"] == 1999
    assert movie["tmdb_poster_path"] == "/poster.jpg"
    assert movie["tmdb_backdrop_path"] == "/backdrop.jpg"
    assert movie["imdb_id"] == "tt0137523"
    assert movie["tmdb_id"] == 550


@pytest.mark.asyncio
@respx.mock
async def test_fetch_imdb_movie_not_found():
    respx.get("https://api.themoviedb.org/3/find/tt9999999").mock(
        return_value=Response(
            200,
            json={"movie_results": []},
        )
    )

    client = UpstreamClient()
    with pytest.raises(LookupError):
        await client.fetch_imdb_movie("tt9999999")


@pytest.mark.asyncio
@respx.mock
async def test_upstream_search():
    respx.get("https://api.themoviedb.org/3/search/multi").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "id": 550,
                        "media_type": "movie",
                        "title": "Fight Club",
                        "release_date": "1999-10-15",
                    },
                    {
                        "id": 1399,
                        "media_type": "tv",
                        "name": "Game of Thrones",
                        "first_air_date": "2011-04-17",
                    },
                ]
            },
        )
    )
    respx.get("https://api.themoviedb.org/3/movie/550/external_ids").mock(
        return_value=Response(200, json={"id": 550, "imdb_id": "tt0137523"})
    )
    respx.get("https://api.themoviedb.org/3/tv/1399/external_ids").mock(
        return_value=Response(200, json={"id": 1399, "imdb_id": "tt0944947"})
    )

    client = UpstreamClient()
    results = await client.fetch_tmdb_search("Fight", language="en-US")

    assert len(results) == 2
    assert results[0]["id"] == "550"
    assert results[0]["imdb_id"] == "tt0137523"
    assert results[1]["id"] == "1399"
    assert results[1]["imdb_id"] == "tt0944947"
