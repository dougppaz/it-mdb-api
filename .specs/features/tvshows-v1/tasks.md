# Tasks: TV Shows (Series) v1 Endpoints

**Design**: none
**Status**: Done
**Approved**: 2025-05-18 - user: "vamos implementar os endpoints para series (tvshows). o schema deve ser igual ao de filme."
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

### Phase 1: TV Shows Implementation

```
T1 -> T2 -> T3 -> T4 -> T5 -> T6 -> T7
```

---

## Task Breakdown

### T1: Create TV Show v1 JSON Schema

**What**: Create JSON schema `definitions/schemas/tvshow-v1.json` identical to `movie-v1.json`.
**Where**: `definitions/schemas/tvshow-v1.json`
**Depends on**: none
**Requirement**: TS-01

**Done when**:
- [x] Schema `definitions/schemas/tvshow-v1.json` is created with properties identical to `movie-v1.json`.

**Tests**: none
**Gate**: quick

---

### T2: Create TV Show Parsers (TMDB & IMDb)

**What**: Implement parser scripts `definitions/parsers/tmdb_tvshow.py` and `definitions/parsers/imdb_tvshow.py`.
**Where**: `definitions/parsers/tmdb_tvshow.py`, `definitions/parsers/imdb_tvshow.py`
**Depends on**: T1
**Requirement**: TS-02

**Done when**:
- [x] Parsers successfully parse raw TV show payloads into standardized schema format.

**Tests**: unit
**Gate**: quick

---

### T3: Create TV Show Resource YAML Definitions

**What**: Create YAML endpoint resource configurations `definitions/resources/v1/tvshows-tmdb.yml` and `definitions/resources/v1/tvshows-imdb.yml`.
**Where**: `definitions/resources/v1/tvshows-tmdb.yml`, `definitions/resources/v1/tvshows-imdb.yml`
**Depends on**: T2
**Requirement**: TS-01

**Done when**:
- [x] Resource definitions correctly point to `tvshow-v1.json` and respective parsers.

**Tests**: none
**Gate**: quick

---

### T4: Add Upstream Client Methods for TV Shows

**What**: Implement `fetch_tmdb_tvshow` and `fetch_imdb_tvshow` in `UpstreamClient` (`it_mdb_api/services/upstream.py`).
**Where**: `it_mdb_api/services/upstream.py`
**Depends on**: T3
**Requirement**: TS-03

**Done when**:
- [x] Upstream client fetches TV show details and external IDs from TMDB and invokes parsers.

**Tests**: unit
**Gate**: quick

---

### T5: Update Worker and Runner for TV Shows Queue

**What**: Update `it_mdb_api/worker.py` and `run.py` to process tasks from `tasks:tvshows` queue.
**Where**: `it_mdb_api/worker.py`, `run.py`
**Depends on**: T4
**Requirement**: TS-03, TS-04

**Done when**:
- [x] Worker processes queue tasks for TV shows and caches results.

**Tests**: integration
**Gate**: full

---

### T6: Implement TV Show API Endpoints & Aliases

**What**: Implement GET endpoints for `/v1/tvshows/{tmdb_id}`, `/v1/tvshows/tt{imdb_id}`, and aliases `/v1/series/...` in `it_mdb_api/api/v1/endpoints.py`.
**Where**: `it_mdb_api/api/v1/endpoints.py`
**Depends on**: T5
**Requirement**: TS-03, TS-04

**Done when**:
- [x] API endpoints handle cache check, queue wait, and timeout for TV shows and series.

**Tests**: integration
**Gate**: full

---

### T7: Add Unit and Integration Tests

**What**: Add unit tests for TV show parsers and integration tests for endpoints and worker in `tests/`.
**Where**: `tests/unit/test_parsers.py`, `tests/integration/test_endpoints.py`, `tests/integration/test_worker.py`
**Depends on**: T6
**Requirement**: TS-05

**Done when**:
- [x] `pytest` passes with 100% success.

**Tests**: integration
**Gate**: build

---

## Checks

**C1** - `definitions/schemas/tvshow-v1.json` has the same structure as `movie-v1.json` (TS-01, AC 1)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_tmdb_tvshow`

**C2** - `tmdb_tvshow.py` and `imdb_tvshow.py` parse raw inputs correctly (TS-02, AC 2)
Proof: `pytest tests/unit/test_parsers.py -k test_parse`

**C3** - Endpoints `/v1/tvshows/{tmdb_id}` and `/v1/series/{tmdb_id}` retrieve TV shows (TS-03, AC 3)
Proof: `pytest tests/integration/test_endpoints.py -k test_get_tmdb_tvshow`

**C4** - Endpoints `/v1/tvshows/tt{imdb_id}` and `/v1/series/tt{imdb_id}` retrieve TV shows by IMDb ID (TS-04, AC 4)
Proof: `pytest tests/integration/test_endpoints.py -k test_get_imdb_tvshow`

**C5** - Full test suite passes successfully (TS-05, AC 5)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
