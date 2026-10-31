# tvshows-v1 proofs

**HEAD**: 5008660
**Tree**: clean
**Result**: 7 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_parsers.py -k test_parse_tmdb_tvshow` | 1 | 1 | pass |
| C2 | `pytest tests/unit/test_parsers.py -k test_parse` | 4 | 4 | pass |
| C3 | `pytest tests/integration/test_endpoints.py -k test_get_tmdb_tvshow` | 1 | 1 | pass |
| C4 | `pytest tests/integration/test_endpoints.py -k test_get_imdb_tvshow` | 1 | 1 | pass |
| C5 | `pytest` | 11 | 11 | pass |
| Build | `pytest` | - | - | pass |
| Build | `ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
