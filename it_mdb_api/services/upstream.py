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
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        headers = {
            "Authorization": f"Bearer {settings.tmdb.tmdb_api_read_access_token}",
            "accept": "application/json",
        }
        params = {"language": language}

        client = await self._get_client()
        # Close client if created locally and not passed in
        should_close = self._client is None
        try:
            response = await client.get(url, headers=headers, params=params)
        finally:
            if should_close:
                await client.aclose()

        if response.status_code == 404:
            raise LookupError(f"TMDB movie {tmdb_id} not found")

        response.raise_for_status()
        raw_data = response.json()
        return parse_tmdb_movie({"movie": raw_data})
