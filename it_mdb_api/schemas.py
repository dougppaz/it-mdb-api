from typing import Optional
from pydantic import BaseModel


class MovieV1(BaseModel):
    id: str
    title: str
    original_title: Optional[str] = None
    year: Optional[int] = None
    overview: Optional[str] = None
    tmdb_poster_path: Optional[str] = None
    tmdb_backdrop_path: Optional[str] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None


class TVShowV1(BaseModel):
    id: str
    title: str
    original_title: Optional[str] = None
    year: Optional[int] = None
    overview: Optional[str] = None
    tmdb_poster_path: Optional[str] = None
    tmdb_backdrop_path: Optional[str] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
