from it_mdb_api.schemas import MovieV1, TVShowV1


def test_movie_v1_validation_success():
    data = {
        "id": "123",
        "title": "Test Movie",
        "original_title": "Test Movie Original",
        "year": 2026,
        "overview": "A test movie overview.",
        "tmdb_poster_path": "/poster.jpg",
        "tmdb_backdrop_path": "/backdrop.jpg",
        "imdb_id": "tt1234567",
        "tmdb_id": 123,
    }
    movie = MovieV1(**data)
    assert movie.id == "123"
    assert movie.title == "Test Movie"
    assert movie.year == 2026
    assert movie.imdb_id == "tt1234567"
    assert movie.tmdb_id == 123


def test_movie_v1_optional_fields_null():
    data = {
        "id": "123",
        "title": "Test Movie",
        "original_title": None,
        "year": None,
        "overview": "",
        "tmdb_poster_path": None,
        "tmdb_backdrop_path": None,
        "imdb_id": None,
        "tmdb_id": None,
    }
    movie = MovieV1(**data)
    assert movie.id == "123"
    assert movie.title == "Test Movie"
    assert movie.original_title is None
    assert movie.year is None
    assert movie.imdb_id is None
    assert movie.tmdb_id is None


def test_tvshow_v1_validation_success():
    data = {
        "id": "456",
        "title": "Test TV Show",
        "original_title": "Test TV Show Original",
        "year": 2025,
        "overview": "A test tv show overview.",
        "tmdb_poster_path": "/poster_tv.jpg",
        "tmdb_backdrop_path": "/backdrop_tv.jpg",
        "imdb_id": "tt7654321",
        "tmdb_id": 456,
    }
    show = TVShowV1(**data)
    assert show.id == "456"
    assert show.title == "Test TV Show"
    assert show.year == 2025
    assert show.imdb_id == "tt7654321"
    assert show.tmdb_id == 456
