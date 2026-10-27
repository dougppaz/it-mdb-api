# add-movie-v1-external-ids proofs

**HEAD**: df14d71
**Tree**: clean
**Result**: 10 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_parsers.py -k test_parse_tmdb_named_input` | 1 | 1 | pass |
| C2 | `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_success` | 1 | 1 | pass |
| C3 | `pytest tests/unit/test_parsers.py -k test_parse_tmdb_named_input` | 1 | 1 | pass |
| C4 | `pytest tests/unit/test_parsers.py -k test_parse_imdb_named_input` | 1 | 1 | pass |
| C5 | `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_success` | 1 | 1 | pass |
| C6 | `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_not_found` | 1 | 1 | pass |
| C7 | `pytest tests/integration/test_endpoints.py -k test_get_tmdb_movie_cache_hit` | 1 | 1 | pass |
| C8 | `pytest` | 7 | 7 | pass |
| Build | `pytest` | - | - | pass |
| Build | `ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
