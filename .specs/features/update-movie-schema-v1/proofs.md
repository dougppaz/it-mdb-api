# update-movie-schema-v1 proofs

**HEAD**: f415740
**Tree**: dirty - definitions/parsers/imdb_movie.py, definitions/parsers/tmdb_movie.py, definitions/schemas/movie-v1.json, tests/integration/test_caching_queue.py, tests/integration/test_worker.py
**Result**: 5 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_upstream.py` | 2 | 2 | pass |
| C2 | `pytest tests/unit/test_upstream.py` | 2 | 2 | pass |
| C3 | `pytest` | 2 | 2 | pass |
| Build | `pytest` | - | - | pass |
| Build | `python3 -m ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
