# search-v1 proofs

**HEAD**: 810720a
**Tree**: clean
**Result**: 6 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_parsers.py -k test_parse_tmdb_search` | 1 | 1 | pass |
| C2 | `pytest tests/unit/test_upstream.py -k test_upstream_search` | 1 | 1 | pass |
| C3 | `pytest tests/integration/test_endpoints.py -k test_search_endpoint` | 1 | 1 | pass |
| C4 | `pytest` | 19 | 19 | pass |
| Build | `pytest` | - | - | pass |
| Build | `ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
