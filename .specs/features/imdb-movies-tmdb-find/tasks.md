# Implement IMDb Movies Endpoint via TMDB Find Tasks

**Design**: none
**Status**: Approved
**Approved**: 2026-10-27 - user: "sim"
**Mutations**: 0
**Build**: `pytest; ruff check it_mdb_api/ definitions/ tests/`

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Resource Definition | none | - (build gate only) | `definitions/` | `pytest; ruff check definitions/` |
| Parsers | unit | 1:1 to spec requirements | `tests/unit/test_parsers.py` | `pytest tests/unit/test_parsers.py` |
| Upstream Client | unit | 1:1 to spec requirements | `tests/unit/test_upstream.py` | `pytest tests/unit/test_upstream.py` |
| Worker / Endpoints | integration | Happy path + edge cases | `tests/integration/` | `pytest tests/integration/` |

## Gate Check Commands

| Gate Level | When to Use | Command |
| --- | --- | --- |
| Quick | After parser / unit test tasks | `pytest tests/unit/` |
| Full | After upstream client & integration test tasks | `pytest` |
| Build | After all tasks | `pytest; ruff check it_mdb_api/ definitions/ tests/` |

---

## Execution Plan

### Phase 1: Definitions, Client, Worker and Endpoint

```
T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7 -> T8 -> T9
```

---

## Task Breakdown

### T1: Update Resource Definition `movies-imdb.yml`

**What**: Add `behavior.upstream.find` referencing `/find/{imdb_id}` with `external_source: imdb_id` in `definitions/resources/v1/movies-imdb.yml`.
**Where**: `definitions/resources/v1/movies-imdb.yml`
**Depends on**: none
**Requirement**: RES-02

**Done when**:
- [x] `behavior.upstream.find` is declared in `definitions/resources/v1/movies-imdb.yml`.

**Tests**: none
**Gate**: quick

---

### T2: Update IMDb Parser `imdb_movie.py`

**What**: Update `definitions/parsers/imdb_movie.py` to extract movie details from `find.movie_results`.
**Where**: `definitions/parsers/imdb_movie.py`
**Depends on**: T1
**Requirement**: PARS-02

**Done when**:
- [ ] Parser extracts movie fields from `find.movie_results[0]`, preserving backwards compatibility with legacy format.

**Tests**: unit
**Gate**: quick

---

### T3: Update Parser Unit Tests

**What**: Add test in `tests/unit/test_parsers.py` for parsing TMDB find response into `movie-v1` format.
**Where**: `tests/unit/test_parsers.py`
**Depends on**: T2
**Requirement**: TEST-02

**Done when**:
- [ ] `test_parse_imdb_find_named_input` passes asserting all `movie-v1` fields.

**Tests**: unit
**Gate**: quick

---

### T4: Add `fetch_imdb_movie` in Upstream Client

**What**: Implement `fetch_imdb_movie(self, imdb_id: str, language: str = "en")` calling `/find/{imdb_id}` in `it_mdb_api/services/upstream.py`.
**Where**: `it_mdb_api/services/upstream.py`
**Depends on**: T3
**Requirement**: UPSTR-02

**Done when**:
- [ ] `fetch_imdb_movie` queries TMDB find endpoint and raises `LookupError` if empty or 404.

**Tests**: unit
**Gate**: quick

---

### T5: Add Upstream Unit Tests for `fetch_imdb_movie`

**What**: Add unit tests in `tests/unit/test_upstream.py` for `fetch_imdb_movie` success and not found scenarios.
**Where**: `tests/unit/test_upstream.py`
**Depends on**: T4
**Requirement**: TEST-02

**Done when**:
- [ ] Unit tests for `fetch_imdb_movie` pass with respx mocks.

**Tests**: unit
**Gate**: quick

---

### T6: Update Worker for IMDb Tasks

**What**: Update `it_mdb_api/worker.py` to inspect `imdb_id` in task payload and call `fetch_imdb_movie`.
**Where**: `it_mdb_api/worker.py`
**Depends on**: T5
**Requirement**: WORK-01

**Done when**:
- [ ] Worker dispatches tasks containing `imdb_id` to `fetch_imdb_movie`.

**Tests**: integration
**Gate**: full

---

### T7: Add Worker Integration Test for IMDb Task

**What**: Add integration test in `tests/integration/test_worker.py` verifying worker processing an IMDb task.
**Where**: `tests/integration/test_worker.py`
**Depends on**: T6
**Requirement**: TEST-02

**Done when**:
- [ ] Integration test passes verifying cached IMDb movie details and readiness notification.

**Tests**: integration
**Gate**: full

---

### T8: Add IMDb Endpoint Route in `endpoints.py`

**What**: Add route `@router.get("/movies/tt{imdb_id}")` in `it_mdb_api/api/v1/endpoints.py`.
**Where**: `it_mdb_api/api/v1/endpoints.py`
**Depends on**: T7
**Requirement**: ROUTE-01

**Done when**:
- [ ] Route `/v1/movies/tt{imdb_id}` handles cache hit, dedup locking, task enqueueing, and timeout.

**Tests**: integration
**Gate**: full

---

### T9: Add Endpoint Integration Tests for IMDb

**What**: Add integration tests in `tests/integration/test_endpoints.py` covering IMDb cache hit and timeout.
**Where**: `tests/integration/test_endpoints.py`
**Depends on**: T8
**Requirement**: TEST-02

**Done when**:
- [ ] Integration tests pass for `/v1/movies/tt{imdb_id}`.
- [ ] `pytest` passes across all test suites.

**Tests**: integration
**Gate**: full

---

## Checks

**C1** - `definitions/resources/v1/movies-imdb.yml` declares `find` under `behavior.upstream` (RES-02, AC 1)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_success`

**C2** - `imdb_movie.py` parses `find` output into `movie-v1` format (PARS-02, AC 2)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_imdb_find_named_input`

**C3** - `UpstreamClient.fetch_imdb_movie` calls TMDB find endpoint (UPSTR-02, AC 3)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_success`

**C4** - `UpstreamClient.fetch_imdb_movie` raises `LookupError` when movie is not found (UPSTR-02, AC 4)
Proof: `pytest tests/unit/test_upstream.py -k test_fetch_imdb_movie_not_found`

**C5** - Worker processes tasks with `imdb_id` and caches under `movie:imdb:` (WORK-01, AC 5)
Proof: `pytest tests/integration/test_worker.py -k test_worker_processes_imdb_queue_item`

**C6** - Endpoint `/v1/movies/tt{imdb_id}` returns movie details (ROUTE-01, AC 6)
Proof: `pytest tests/integration/test_endpoints.py -k test_get_imdb_movie_cache_hit`

**C7** - All test suites pass with 100% pass rate (TEST-02, AC 7)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
