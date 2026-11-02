from pydantic import BaseModel


class MovieV1(BaseModel):
    id: str
    title: str
    original_title: str | None = None
    year: int | None = None
    overview: str | None = None
    tmdb_poster_path: str | None = None
    tmdb_backdrop_path: str | None = None
    imdb_id: str | None = None
    tmdb_id: int | None = None


class TVShowV1(BaseModel):
    id: str
    title: str
    original_title: str | None = None
    year: int | None = None
    overview: str | None = None
    tmdb_poster_path: str | None = None
    tmdb_backdrop_path: str | None = None
    imdb_id: str | None = None
    tmdb_id: int | None = None


class SearchItemV1(BaseModel):
    id: str
    title: str
    original_title: str | None = None
    year: int | None = None
    overview: str | None = None
    tmdb_poster_path: str | None = None
    tmdb_backdrop_path: str | None = None
    imdb_id: str | None = None
    tmdb_id: int | None = None
    media_type: str | None = None
