# Update Movie Schema v1 Tasks

**Design**: none
**Status**: Approved
**Approved**: 2025-05-18 - user: "vamos ajustar o schema de movie-v1: remova o campo genres e rating. adicione os campos tmdb_poster_path e tmdb_backdrop_path."
**Mutations**: 3
**Build**: `pytest; python3 -m ruff check it_mdb_api/ definitions/ tests/`

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| Schema / Parser | unit | 1:1 to spec requirements | `tests/unit/test_upstream.py` | `pytest tests/unit/test_upstream.py` |
| Integration | integration | Happy path + edge cases | `tests/integration/` | `pytest tests/integration/` |

## Gate Check Commands

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | After unit test tasks | `pytest tests/unit/` |
| Full | After integration test tasks | `pytest` |
| Build | After all tasks | `pytest; ruff check .` |

---

## Execution Plan

### Phase 1: All Tasks

```
T1 → T2 → T3 → T4 → T5 → T6
```

---

## Task Breakdown

### T1: Update JSON Schema `movie-v1.json`

**What**: Remove `genres` and `rating` properties, and add `tmdb_poster_path` and `tmdb_backdrop_path` properties to `definitions/schemas/movie-v1.json`.
**Where**: `definitions/schemas/movie-v1.json`
**Depends on**: None
**Requirement**: SCHEM-01

**Done when**:
- [ ] Schema `definitions/schemas/movie-v1.json` updated without `genres` and `rating`, with `tmdb_poster_path` and `tmdb_backdrop_path`.

**Tests**: none
**Gate**: quick

---

### T2: Update TMDB Parser

**What**: Update TMDB parser to output `tmdb_poster_path` and `tmdb_backdrop_path` and remove `genres` and `rating`.
**Where**: `definitions/parsers/tmdb_movie.py`
**Depends on**: T1
**Requirement**: PARS-01

**Done when**:
- [ ] `tmdb_movie.py` parses `poster_path` and `backdrop_path` into `tmdb_poster_path` and `tmdb_backdrop_path`.

**Tests**: unit
**Gate**: quick

---

### T3: Update IMDb Parser

**What**: Update IMDb parser to remove `genres` and `rating`, setting `tmdb_poster_path` and `tmdb_backdrop_path` to `None`.
**Where**: `definitions/parsers/imdb_movie.py`
**Depends on**: T2
**Requirement**: PARS-01

**Done when**:
- [ ] `imdb_movie.py` sets `tmdb_poster_path` and `tmdb_backdrop_path` to `None` and drops `genres`/`rating`.

**Tests**: unit
**Gate**: quick

---

### T4: Update Unit Test

**What**: Update unit test assertions for upstream parser/client.
**Where**: `tests/unit/test_upstream.py`
**Depends on**: T3
**Requirement**: TEST-01

**Done when**:
- [ ] `test_upstream.py` uses `tmdb_poster_path` and `tmdb_backdrop_path` instead of `genres` and `rating`.

**Tests**: unit
**Gate**: quick

---

### T5: Update Worker Integration Test

**What**: Update worker integration test mock data.
**Where**: `tests/integration/test_worker.py`
**Depends on**: T4
**Requirement**: TEST-01

**Done when**:
- [ ] `test_worker.py` uses new schema fields.

**Tests**: integration
**Gate**: full

---

### T6: Update Caching Queue Integration Test

**What**: Update caching queue integration test mock data.
**Where**: `tests/integration/test_caching_queue.py`
**Depends on**: T5
**Requirement**: TEST-01

**Done when**:
- [ ] `test_caching_queue.py` uses new schema fields.
- [ ] `pytest` passes successfully across all tests.

**Tests**: integration
**Gate**: full

---

## Checks

**C1** - `definitions/schemas/movie-v1.json` contains `tmdb_poster_path` and `tmdb_backdrop_path` and lacks `genres` and `rating` (SCHEM-01, AC 1-2)
Proof: `pytest tests/unit/test_upstream.py`

**C2** - Parsers correctly output `tmdb_poster_path` and `tmdb_backdrop_path` (PARS-01, AC 3-4)
Proof: `pytest tests/unit/test_upstream.py`

**C3** - All tests pass successfully (TEST-01, AC 5)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
