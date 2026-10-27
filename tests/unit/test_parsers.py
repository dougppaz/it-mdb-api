import pytest
from definitions.parsers.tmdb_movie import parse as parse_tmdb
from definitions.parsers.imdb_movie import parse as parse_imdb


def test_parse_tmdb_named_input():
    named_input = {
        "movie": {
            "id": 550,
            "title": "Fight Club",
            "release_date": "1999-10-15",
            "overview": "Mischief, Mayhem, Soap.",
            "poster_path": "/poster.jpg",
            "backdrop_path": "/backdrop.jpg",
        }
    }
    result = parse_tmdb(named_input)
    assert result["id"] == "550"
    assert result["title"] == "Fight Club"
    assert result["year"] == 1999
    assert result["tmdb_poster_path"] == "/poster.jpg"


def test_parse_imdb_named_input():
    named_input = {
        "movie": {
            "tconst": "tt0137523",
            "primaryTitle": "Fight Club",
            "startYear": "1999",
            "description": "An insomniac office worker...",
        }
    }
    result = parse_imdb(named_input)
    assert result["id"] == "tt0137523"
    assert result["title"] == "Fight Club"
    assert result["year"] == 1999
    assert result["tmdb_poster_path"] is None
