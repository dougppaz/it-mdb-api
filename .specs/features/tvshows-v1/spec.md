# TV Shows (Series) v1 Endpoints Specification

**Approved**: 2025-05-18 - user: "vamos implementar os endpoints para series (tvshows). o schema deve ser igual ao de filme."

## Problem Statement

The API currently supports movie endpoints (`/v1/movies/...`), but lacks TV show / series endpoints (`/v1/tvshows/...` and `/v1/series/...`) along with their JSON schemas, resource definitions, parser scripts, upstream client methods, and queue/worker handling.

## Goals

- [ ] Create `definitions/schemas/tvshow-v1.json` with the exact same structure as `movie-v1.json`.
- [ ] Create `definitions/resources/v1/tvshows-tmdb.yml` for TMDB TV show lookup by ID.
- [ ] Create `definitions/resources/v1/tvshows-imdb.yml` for IMDb TV show lookup via TMDB find.
- [ ] Create parser `definitions/parsers/tmdb_tvshow.py`.
- [ ] Create parser `definitions/parsers/imdb_tvshow.py`.
- [ ] Add `fetch_tmdb_tvshow` and `fetch_imdb_tvshow` methods to `UpstreamClient` in `it_mdb_api/services/upstream.py`.
- [ ] Update `it_mdb_api/worker.py` to process TV show queue tasks (`tasks:tvshows`).
- [ ] Implement API endpoints in `it_mdb_api/api/v1/endpoints.py` for `/v1/tvshows/{tmdb_id}`, `/v1/tvshows/tt{imdb_id}`, and aliases `/v1/series/{tmdb_id}`, `/v1/series/tt{imdb_id}`.
- [ ] Add comprehensive unit and integration tests for TV show parsers, upstream client, and endpoints.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Seasons and episodes sub-resources | Out of scope for base TV show v1 endpoint implementation. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Schema structure | Identical to `movie-v1.json` | Explicitly requested by user ("o schema deve ser igual ao de filme"). | y |
| Endpoint paths | `/v1/tvshows/...` and alias `/v1/series/...` | Covers both terminology preferences for tv shows / series. | y |
| Queue name | `tasks:tvshows` (and consumed by worker) | Keeps task queues organized separately from movies. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: TV Shows / Series v1 Endpoints & Caching Flow ⭐ MVP

**User Story**: As an API consumer, I want to request TV show details by TMDB ID or IMDb ID using `/v1/tvshows/...` or `/v1/series/...`, so that I can retrieve cached TV show information efficiently.

**Acceptance Criteria**:

1. WHEN `definitions/schemas/tvshow-v1.json` is inspected, THEN it SHALL have the same properties and structure as `movie-v1.json`.
2. WHEN parser `tmdb_tvshow.py` or `imdb_tvshow.py` is executed, THEN it SHALL parse raw TMDB/IMDb TV show responses into the standardized schema format.
3. WHEN `GET /v1/tvshows/{tmdb_id}` or `GET /v1/series/{tmdb_id}` is requested, THEN the API SHALL return cached data or enqueue a task to fetch TV show details from TMDB.
4. WHEN `GET /v1/tvshows/tt{imdb_id}` or `GET /v1/series/tt{imdb_id}` is requested, THEN the API SHALL return cached data or enqueue a task to find the TV show by IMDb ID.
5. All test suites in `tests/` SHALL pass successfully.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| TS-01 | P1 | Tasks | Pending |
| TS-02 | P1 | Tasks | Pending |
| TS-03 | P1 | Tasks | Pending |
| TS-04 | P1 | Tasks | Pending |
| TS-05 | P1 | Tasks | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `ruff` passes with 0 errors.
