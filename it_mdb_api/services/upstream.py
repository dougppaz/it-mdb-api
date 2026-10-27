import asyncio

import httpx

from definitions.parsers.tmdb_movie import parse as parse_tmdb_movie
from it_mdb_api.settings import settings


class UpstreamClient:
    def __init__(self, client: httpx.AsyncClient | None = None):
        self._client = client

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is not None:
            return self._client
        return httpx.AsyncClient(timeout=10.0)

    async def fetch_tmdb_movie(self, tmdb_id: int, language: str = "en-US") -> dict:
        movie_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        ext_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids"
        headers = {
            "Authorization": f"Bearer {settings.tmdb.tmdb_api_read_access_token}",
            "accept": "application/json",
        }
        params = {"language": language}

        client = await self._get_client()
        # Close client if created locally and not passed in
        should_close = self._client is None
        try:
            movie_resp, ext_resp = await asyncio.gather(
                client.get(movie_url, headers=headers, params=params),
                client.get(ext_url, headers=headers),
                return_exceptions=True,
            )
        finally:
            if should_close:
                await client.aclose()

        if isinstance(movie_resp, Exception):
            raise movie_resp

        if movie_resp.status_code == 404:
            raise LookupError(f"TMDB movie {tmdb_id} not found")

        movie_resp.raise_for_status()
        raw_movie_data = movie_resp.json()

        if not isinstance(ext_resp, Exception) and ext_resp.status_code == 200:
            raw_ext_data = ext_resp.json()
        else:
            raw_ext_data = {}

        return parse_tmdb_movie({"movie": raw_movie_data, "external_ids": raw_ext_data})
