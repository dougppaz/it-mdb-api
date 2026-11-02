# Tasks: Search API v1 Endpoint

**Design**: none
**Status**: In Progress
**Approved**: 2025-02-20 - user: "criacao das especificacoes e implementacao do novo endpoint"
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

### Phase 1: Search Implementation

```
T1 -> T2 -> T3 -> T4 -> T5
```

---

## Task Breakdown

### T1: Add Unit Tests for Search Parser

**What**: Add unit test for `definitions/parsers/tmdb_search.py` in `tests/unit/test_parsers.py`.
**Where**: `tests/unit/test_parsers.py`
**Depends on**: none
**Requirement**: SRCH-02

**Done when**:
- [x] `test_parse_tmdb_search` passes successfully asserting list of `search-item-v1` items.

**Tests**: unit
**Gate**: quick

---

### T2: Add Upstream Client Method for Search (`upstream_items`)

**What**: Implement `fetch_tmdb_search` in `UpstreamClient` (`it_mdb_api/services/upstream.py`) handling `/search/multi` and iterating over results to fetch external IDs for movies and TV shows based on `upstream_items` spec.
**Where**: `it_mdb_api/services/upstream.py`
**Depends on**: T1
**Requirement**: SRCH-03

**Done when**:
- [ ] Upstream client fetches search results and dispatches per-item external ID calls, invoking `tmdb_search.py` parser.

**Tests**: unit
**Gate**: quick

---

### T3: Update Worker for Search Queue

**What**: Update `it_mdb_api/worker.py` to process tasks from `tasks:search` queue.
**Where**: `it_mdb_api/worker.py`
**Depends on**: T2
**Requirement**: SRCH-03

**Done when**:
- [ ] Worker processes queue tasks for search and caches results.

**Tests**: integration
**Gate**: full

---

### T4: Implement Search API Endpoint

**What**: Implement GET `/v1/search` endpoint in `it_mdb_api/api/v1/endpoints.py`.
**Where**: `it_mdb_api/api/v1/endpoints.py`
**Depends on**: T3
**Requirement**: SRCH-01, SRCH-03

**Done when**:
- [ ] API endpoint handles cache check, queue wait, and timeout for search queries.

**Tests**: integration
**Gate**: full

---

### T5: Add Endpoints & Worker Integration Tests for Search

**What**: Add integration tests for search endpoint and worker in `tests/`.
**Where**: `tests/integration/test_endpoints.py`, `tests/integration/test_worker.py`
**Depends on**: T4
**Requirement**: SRCH-04

**Done when**:
- [ ] `pytest` passes with 100% success.

**Tests**: integration
**Gate**: build

---

## Checks

**C1** - `tmdb_search.py` parses multi-search and external IDs into `search-item-v1` format (SRCH-02, AC 2)
Proof: `pytest tests/unit/test_parsers.py -k test_parse_tmdb_search`

**C2** - Upstream client fetches search and item external IDs using `upstream_items` (SRCH-03, AC 3)
Proof: `pytest tests/unit/test_upstream.py -k test_upstream_search`

**C3** - Endpoint `/v1/search` retrieves search results with caching and queueing (SRCH-01, AC 3)
Proof: `pytest tests/integration/test_endpoints.py -k test_search_endpoint`

**C4** - Full test suite passes successfully (SRCH-04, AC 4)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
