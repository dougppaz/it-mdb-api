from definitions.parsers.imdb_movie import parse as parse_imdb
from definitions.parsers.tmdb_movie import parse as parse_tmdb


def test_parse_tmdb_named_input():
    named_input = {
        "movie": {
            "id": 550,
            "title": "Fight Club",
            "release_date": "1999-10-15",
            "overview": "Mischief, Mayhem, Soap.",
            "poster_path": "/poster.jpg",
            "backdrop_path": "/backdrop.jpg",
        },
        "external_ids": {
            "id": 550,
            "imdb_id": "tt0137523",
        },
    }
    result = parse_tmdb(named_input)
    assert result["id"] == "550"
    assert result["title"] == "Fight Club"
    assert result["year"] == 1999
    assert result["tmdb_poster_path"] == "/poster.jpg"
    assert result["imdb_id"] == "tt0137523"
    assert result["tmdb_id"] == 550


def test_parse_imdb_find_named_input():
    named_input = {
        "find": {
            "movie_results": [
                {
                    "id": 550,
                    "title": "Fight Club",
                    "release_date": "1999-10-15",
                    "overview": "Mischief, Mayhem, Soap.",
                    "poster_path": "/poster.jpg",
                    "backdrop_path": "/backdrop.jpg",
                    "imdb_id": "tt0137523",
                }
            ]
        }
    }
    result = parse_imdb(named_input)
    assert result["id"] == "550"
    assert result["title"] == "Fight Club"
    assert result["year"] == 1999
    assert result["tmdb_poster_path"] == "/poster.jpg"
    assert result["tmdb_backdrop_path"] == "/backdrop.jpg"
    assert result["imdb_id"] == "tt0137523"
    assert result["tmdb_id"] == 550

