# Add Movie v1 External IDs Tasks

**Design**: none
**Status**: Approved
**Approved**: 2026-10-27 - user: "vamos so corrigir para que o imdb_id seja string.. e pode seguir pra implementacao. ambos campos novos podem ser nulos."
**Mutations**: 0
**Build**: `pytest; ruff check it_mdb_api/ definitions/ tests/`

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Schema / Resource Definition | none | - (build gate only) | `definitions/` | `pytest; ruff check definitions/` |
| Parsers | unit | 1:1 to spec requirements | `tests/unit/test_parsers.py` | `pytest tests/unit/test_parsers.py` |
| Upstream Client | unit | 1:1 to spec requirements | `tests/unit/test_upstream.py` | `pytest tests/unit/test_upstream.py` |
| Integration | integration | Happy path + edge cases | `tests/integration/` | `pytest tests/integration/` |

## Gate Check Commands

| Gate Level | When to Use | Command |
| --- | --- | --- |
| Quick | After parser / unit test tasks | `pytest tests/unit/` |
| Full | After upstream client & integration test tasks | `pytest` |
| Build | After all tasks | `pytest; ruff check it_mdb_api/ definitions/ tests/` |

---

## Execution Plan

### Phase 1: Definitions and Code Updates

```
T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8 -> T9
```

---

## Task Breakdown

### T1: Update JSON Schema `movie-v1.json`

**What**: Add `imdb_id` (string or null) and `tmdb_id` (integer or null) to properties in `definitions/schemas/movie-v1.json`.
**Where**: `definitions/schemas/movie-v1.json`
**Depends on**: none
**Requirement**: SCHEM-01

**Done when**:
- [x] Schema `definitions/schemas/movie-v1.json` includes `imdb_id` (type `["string", "null"]`) and `tmdb_id` (type `["integer", "null"]`) in properties.

**Tests**: none
**Gate**: quick

---

### T2: Update Resource Definition `movies-tmdb.yml`

**What**: Update `definitions/resources/v1/movies-tmdb.yml` upstream section to include `external_ids` endpoint.
**Where**: `definitions/resources/v1/movies-tmdb.yml`
**Depends on**: T1
**Requirement**: RES-01

**Done when**:
- [x] `behavior.upstream.external_ids` is declared with path `/movie/{tmdb_id}/external_ids`.

**Tests**: none
**Gate**: quick

---

### T3: Update TMDB Parser `tmdb_movie.py`

**What**: Update TMDB parser to extract `imdb_id` from external_ids and `tmdb_id` from movie ID.
**Where**: `definitions/parsers/tmdb_movie.py`
**Depends on**: T2
**Requirement**: PARS-01

**Done when**:
- [x] Parser outputs `imdb_id` as string (or None) and `tmdb_id` as integer (or None).

**Tests**: unit
**Gate**: quick

---

### T4: Update IMDb Parser `imdb_movie.py`

**What**: Update IMDb parser to set `imdb_id` to movie ID/tconst and `tmdb_id` to None.
**Where**: `definitions/parsers/imdb_movie.py`
**Depends on**: T3
**Requirement**: PARS-01

**Done when**:
- [ ] Parser outputs `imdb_id` as string and `tmdb_id` as None.

**Tests**: unit
**Gate**: quick

---

### T5: Update Upstream Client `upstream.py`

**What**: Update `UpstreamClient.fetch_tmdb_movie` to call both `/movie/{tmdb_id}` and `/movie/{tmdb_id}/external_ids`, passing named dictionary to parser.
**Where**: `it_mdb_api/services/upstream.py`
**Depends on**: T4
**Requirement**: UPSTR-01

**Done when**:
- [ ] Upstream client queries external_ids and passes `{"movie": ..., "external_ids": ...}` to `parse_tmdb_movie`.

**Tests**: unit
**Gate**: quick

---

### T6: Update Unit Tests for Parsers

**What**: Update `tests/unit/test_parsers.py` to test TMDB and IMDb parser outputs for `imdb_id` and `tmdb_id`.
**Where**: `tests/unit/test_parsers.py`
**Depends on**: T5
**Requirement**: TEST-01

**Done when**:
- [ ] `test_parsers.py` asserts `imdb_id` and `tmdb_id` on parser outputs and passes.

**Tests**: unit
**Gate**: quick

---

### T7: Update Unit Tests for Upstream Client

**What**: Update `tests/unit/test_upstream.py` to mock `/movie/550/external_ids` and assert `imdb_id` and `tmdb_id`.
**Where**: `tests/unit/test_upstream.py`
**Depends on**: T6
**Requirement**: TEST-01

**Done when**:
- [ ] Upstream unit tests pass with external_ids mock.

**Tests**: unit
**Gate**: quick

---

### T8: Update Worker Integration Test

**What**: Update `tests/integration/test_worker.py` to mock external_ids and assert `imdb_id` and `tmdb_id`.
**Where**: `tests/integration/test_worker.py`
**Depends on**: T7
**Requirement**: TEST-01

**Done when**:
- [ ] `test_worker.py` passes with external_ids mock.

**Tests**: integration
**Gate**: full

---

### T9: Update Caching Queue Integration Test

**What**: Update `tests/integration/test_caching_queue.py` to mock external_ids.
**Where**: `tests/integration/test_caching_queue.py`
**Depends on**: T8
**Requirement**: TEST-01

**Done when**:
- [ ] `test_caching_queue.py` passes with external_ids mock.

**Tests**: integration
**Gate**: full

---

## Checks

**C1** - `definitions/schemas/movie-v1.json` contains `imdb_id` (string or null) and `tmdb_id` (integer or null) (SCHEM-01, AC 1)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_tmdb_named_input`

**C2** - `definitions/resources/v1/movies-tmdb.yml` declares `external_ids` upstream call (RES-01, AC 2)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_success`

**C3** - `tmdb_movie.py` parser parses `imdb_id` and `tmdb_id` (PARS-01, AC 3)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_tmdb_named_input`

**C4** - `imdb_movie.py` parser outputs `imdb_id` and null `tmdb_id` (PARS-01, AC 4)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_imdb_named_input`

**C5** - `UpstreamClient.fetch_tmdb_movie` queries both movie and external_ids (UPSTR-01, AC 5)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_success`

**C6** - `UpstreamClient.fetch_tmdb_movie` raises `LookupError` when movie is 404 (UPSTR-01, AC 6)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_tmdb_movie_not_found`

**C7** - Endpoint `/v1/movies/{tmdb_id}` returns movie with `imdb_id` and `tmdb_id` (TEST-01, AC 7)
Proof: `pytest tests/integration/test_endpoints.py -k test_get_tmdb_movie_cache_hit`

**C8** - Full test suite passes across all unit and integration tests (TEST-01, AC 8)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
