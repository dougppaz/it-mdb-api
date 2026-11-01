# openapi-movie-tvshow-schemas proofs

**HEAD**: d6c1f6e
**Tree**: clean
**Result**: 7 pass, 0 fail; mutations 0 killed, 0 not

| Check | Proof | Ran | Passed | Result |
| --- | --- | --- | --- | --- |
| C1 | `pytest tests/unit/test_schemas.py` | 3 | 3 | pass |
| C2 | `pytest tests/unit/test_schemas.py` | 3 | 3 | pass |
| C3 | `pytest tests/integration/test_endpoints.py` | 7 | 7 | pass |
| C4 | `pytest tests/integration/test_endpoints.py -k test_openapi_schemas` | 1 | 1 | pass |
| C5 | `pytest` | 10 | 10 | pass |
| Build | `pytest` | - | - | pass |
| Build | `ruff check it_mdb_api/ definitions/ tests/` | - | - | pass |
