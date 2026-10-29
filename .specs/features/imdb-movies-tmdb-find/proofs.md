# imdb-movies-tmdb-find proofs

**HEAD**: 91dfb6d
**Tree**: clean
**Result**: 9 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_success` | 1 | 1 | pass |
| C2 | `pytest tests/unit/test_parsers.py -k test_parse_imdb_find_named_input` | 1 | 1 | pass |
| C3 | `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_success` | 1 | 1 | pass |
| C4 | `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_not_found` | 1 | 1 | pass |
| C5 | `pytest tests/integration/test_worker.py -k test_worker_processes_imdb_queue_item` | 1 | 1 | pass |
| C6 | `pytest tests/integration/test_endpoints.py -k test_get_imdb_movie_cache_hit` | 1 | 1 | pass |
| C7 | `pytest` | 11 | 11 | pass |
| Build | `pytest` | - | - | pass |
| Build | `ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
