# OpenAPI Movie and TVShow Response Schemas Tasks

**Design**: none
**Status**: In Progress
**Approved**: 2026-11-01 - user: "aprovado, pode criar as tarefas e seguir para implementacao"
**Mutations**: 0
**Build**: `pytest; ruff check it_mdb_api/ definitions/ tests/`

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Schemas / Models | unit | 1:1 with JSON schemas | `tests/unit/test_schemas.py` | `pytest tests/unit/test_schemas.py` |
| Endpoints / OpenAPI | integration | Schema presence & serialization | `tests/integration/test_endpoints.py` | `pytest tests/integration/test_endpoints.py` |

## Gate Check Commands

| Gate Level | When to Use | Command |
| --- | --- | --- |
| Quick | After unit test tasks | `pytest tests/unit/` |
| Full | After integration test tasks | `pytest` |
| Build | After all tasks | `pytest; ruff check it_mdb_api/ definitions/ tests/` |

---

## Execution Plan

### Phase 1: Schemas, Endpoints, and OpenAPI Integration

```
T1 -> T2 -> T3 -> T4
```

---

## Task Breakdown

### T1: Create Pydantic Models for Movie and TVShow

**What**: Create `it_mdb_api/schemas.py` defining `MovieV1` and `TVShowV1` Pydantic models matching `definitions/schemas/movie-v1.json` and `tvshow-v1.json`.
**Where**: `it_mdb_api/schemas.py`
**Depends on**: none
**Requirement**: OAPI-04

**Done when**:
- [x] `it_mdb_api/schemas.py` contains `MovieV1` and `TVShowV1` with all fields (`id`, `title`, `original_title`, `year`, `overview`, `tmdb_poster_path`, `tmdb_backdrop_path`, `imdb_id`, `tmdb_id`).

**Tests**: unit
**Gate**: quick

---

### T2: Add Schema Unit Tests

**What**: Add unit tests in `tests/unit/test_schemas.py` verifying serialization and validation of `MovieV1` and `TVShowV1`.
**Where**: `tests/unit/test_schemas.py`
**Depends on**: T1
**Requirement**: OAPI-04

**Done when**:
- [x] `tests/unit/test_schemas.py` passes successfully with valid and optional fields.

**Tests**: unit
**Gate**: quick

---

### T3: Update FastAPI Endpoints with Response Models

**What**: Update `it_mdb_api/api/v1/endpoints.py` to annotate all 4 endpoints (`get_imdb_movie`, `get_tmdb_movie`, `get_imdb_tvshow`, `get_tmdb_tvshow`) with `response_model=MovieV1` or `response_model=TVShowV1`.
**Where**: `it_mdb_api/api/v1/endpoints.py`
**Depends on**: T2
**Requirement**: OAPI-02, OAPI-03

**Done when**:
- [ ] All 4 endpoints specify `response_model`.

**Tests**: integration
**Gate**: full

---

### T4: Add OpenAPI Schema Integration Test

**What**: Add test in `tests/integration/test_endpoints.py` asserting OpenAPI `/openapi.json` contains `MovieV1` and `TVShowV1` component schemas.
**Where**: `tests/integration/test_endpoints.py`
**Depends on**: T3
**Requirement**: OAPI-01

**Done when**:
- [ ] Integration test verifies OpenAPI schemas are present and correct.
- [ ] `pytest` passes across all test suites.

**Tests**: integration
**Gate**: full

---

## Checks

**C1** - Pydantic models `MovieV1` and `TVShowV1` are defined in `it_mdb_api/schemas.py` (OAPI-04, AC 4)
Proof: `pytest tests/unit/test_schemas.py`

**C2** - Unit tests pass for schema validation (OAPI-04, AC 4)
Proof: `pytest tests/unit/test_schemas.py`

**C3** - Endpoints in `endpoints.py` use `response_model` (OAPI-02, OAPI-03, AC 2, AC 3)
Proof: `pytest tests/integration/test_endpoints.py`

**C4** - OpenAPI spec exposes `MovieV1` and `TVShowV1` component schemas (OAPI-01, AC 1)
Proof: `pytest tests/integration/test_endpoints.py -k test_openapi_schemas`

**C5** - All test suites pass with 100% pass rate (OAPI-01, AC 1-4)
Proof: `pytest`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none
