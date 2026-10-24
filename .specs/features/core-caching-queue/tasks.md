# Core Caching and Async Queue Architecture Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.**

**Design**: `.specs/features/core-caching-queue/design.md`
**Status**: Draft

---

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| Service | unit | All branches; 1:1 to spec ACs; all listed edge cases | `tests/unit/test_*.py` | `pytest tests/unit` |
| Route / Controller | integration | All routes: happy path + edge cases + timeout / error paths | `tests/integration/test_*.py` | `pytest tests/integration` |
| Worker / Queue | integration | Queue push, deduplication, worker consumption, and cache population | `tests/integration/test_*.py` | `pytest tests/integration` |
| Entity / Config | none | - (build gate only) | - | pytest |

## Gate Check Commands

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | After tasks with unit tests only | `pytest tests/unit` |
| Full | After tasks with e2e/integration tests | `pytest` |
| Build | After phase completion or config/entity-only tasks | `pytest && ruff check .` |

---

## Execution Plan

```
Phase 1 → Phase 2 → Phase 3 → Phase 4

Phase 1:  T1 (Setup) ------→ T2 (Cache Service)
Phase 2:  T3 (Queue Service)
Phase 3:  T4 (IMDb/TMDB Client) ------→ T5 (API Endpoints)
Phase 4:  T6 (Worker) ------→ T7 (Integration Tests)
```

---

## Task Breakdown

### Phase 1: Foundation

#### T1: Initialize Python project structure and dependencies
**What**: Initialize `pyproject.toml`, FastAPI app entrypoint (`src/main.py`), and base directory structure.
**Where**: `pyproject.toml`
**Depends on**: None
**Reuses**: Standard FastAPI project layout
**Requirement**: CORE-01

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [x] `pyproject.toml` created with dependencies (`fastapi`, `uvicorn`, `redis`, `pydantic`, `pytest`, `httpx`, `ruff`)
- [x] `it_mdb_api/main.py` created with FastAPI app instance
- [x] Gate check passes: `pytest`

**Tests**: none
**Gate**: Build

---

#### T2: Implement Redis Cache Service
**What**: Create Redis connection manager and cache service for get/set with TTL and atomic lock (`it_mdb_api/services/cache.py`).
**Where**: `it_mdb_api/services/cache.py`
**Depends on**: T1
**Reuses**: `redis-py` async client

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [x] `CacheService` implemented with `get`, `set`, and `set_nx` methods
- [x] Unit tests pass for cache operations
- [x] Gate check passes: `pytest tests/unit`

**Tests**: unit
**Gate**: Quick

---

### Phase 2: Queue & Synchronization Layer

#### T3: Implement Async Queue & Waiting Mechanism Service
**What**: Create queue pushing, deduplication check, and async waiting/pubsub mechanism for uncached resource requests (`it_mdb_api/services/queue.py`).
**Where**: `it_mdb_api/services/queue.py`
**Depends on**: T2
**Reuses**: `it_mdb_api/services/cache.py`

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [ ] Queue service implemented supporting task enqueue, deduplication, and wait/poll loop with timeout handling
- [ ] Unit tests pass for queue and wait logic
- [ ] Gate check passes: `pytest tests/unit`

**Tests**: unit
**Gate**: Quick

---

### Phase 3: Upstream Client & API Endpoints

#### T4: Implement IMDb/TMDB External API Client & Parser
**What**: Create external API client service to fetch and parse movie, TV show, search, and ID mapping payloads from IMDb/TMDB (`it_mdb_api/services/imdb_tmdb.py`).
**Where**: `it_mdb_api/services/imdb_tmdb.py`
**Depends on**: T2
**Reuses**: `httpx` async client

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [ ] `ImdbTmdbClient` implemented with mockable HTTP calls and response parsers
- [ ] Unit tests pass
- [ ] Gate check passes: `pytest tests/unit`

**Tests**: unit
**Gate**: Quick

---

#### T5: Implement REST API Endpoints with Cache-First & Timeout Handling
**What**: Create API route handlers for movies, TV shows, search, and ID mapping integrating cache check, queue wait, and timeout query parameter handling (`it_mdb_api/api/v1/endpoints.py`).
**Where**: `it_mdb_api/api/v1/endpoints.py`
**Depends on**: T3, T4
**Reuses**: `it_mdb_api/services/cache.py`, `it_mdb_api/services/queue.py`, `it_mdb_api/services/imdb_tmdb.py`

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [ ] Endpoints implemented supporting cache hits, queue wait, `timeout` query parameter, and HTTP 504 on timeout
- [ ] Integration tests pass
- [ ] Gate check passes: `pytest`

**Tests**: integration
**Gate**: Full

---

### Phase 4: Worker & Comprehensive Validation

#### T6: Implement Background Worker Process
**What**: Implement background worker loop that consumes tasks from Redis queue, calls upstream API, parses data, and caches results (`it_mdb_api/worker.py`).
**Where**: `it_mdb_api/worker.py`
**Depends on**: T5
**Reuses**: `it_mdb_api/services/queue.py`, `it_mdb_api/services/imdb_tmdb.py`, `it_mdb_api/services/cache.py`

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [ ] Worker successfully polls queue, executes fetch, caches result, and notifies waiters
- [ ] Gate check passes: `pytest`

**Tests**: integration
**Gate**: Full

---

#### T7: Add Comprehensive End-to-End & Integration Test Suite
**What**: Add robust integration tests covering concurrent requests, cache hits, deduplication, and timeout handling (`tests/integration/test_caching_queue.py`).
**Where**: `tests/integration/test_caching_queue.py`
**Depends on**: T6
**Reuses**: `pytest`, `httpx.AsyncClient`

**Tools**:
- MCP: `filesystem`
- Skill: NONE

**Done when**:
- [ ] Integration tests cover all ACs from specification (cache hit, queue deduplication, wait timeout 504)
- [ ] Full test suite passes
- [ ] Gate check passes: `pytest`

**Tests**: integration
**Gate**: Full

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3 → Phase 4

Phase 1:  T1 ------→ T2
Phase 2:  T3
Phase 3:  T4 ------→ T5
Phase 4:  T6 ------→ T7
```

---

## Task Granularity Check

| Task | Scope | Status |
| - | - | - |
| T1: Init project & dependencies | 1 config file / entrypoint | ✅ Granular |
| T2: Cache Service | 1 service file | ✅ Granular |
| T3: Queue & Wait Service | 1 service file | ✅ Granular |
| T4: IMDb/TMDB Client | 1 service file | ✅ Granular |
| T5: API Endpoints | 1 router file | ✅ Granular |
| T6: Background Worker | 1 script file | ✅ Granular |
| T7: Integration Tests | 1 test suite | ✅ Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| - | - | - | - |
| T1 | None | Start | ✅ Match |
| T2 | T1 | T1 | ✅ Match |
| T3 | T2 | T2 | ✅ Match |
| T4 | T2 | T2 | ✅ Match |
| T5 | T3, T4 | T3, T4 | ✅ Match |
| T6 | T5 | T5 | ✅ Match |
| T7 | T6 | T6 | ✅ Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| - | - | - | - | - |
| T1 | Entity / Config | none | none | ✅ OK |
| T2 | Service | unit | unit | ✅ OK |
| T3 | Service | unit | unit | ✅ OK |
| T4 | Service | unit | unit | ✅ OK |
| T5 | Route / Controller | integration | integration | ✅ OK |
| T6 | Worker / Queue | integration | integration | ✅ OK |
| T7 | Worker / Queue | integration | integration | ✅ OK |
