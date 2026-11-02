# Search API v1 Endpoint Specification

**Approved**: 2025-02-20 - user: "criacao das especificacoes e implementacao do novo endpoint"

## Problem Statement

The API currently supports movie and TV show details endpoints (`/v1/movies/...`, `/v1/tvshows/...`), but lacks a search endpoint (`/v1/search/`) using TMDB multi-search and per-item external IDs fetching via `upstream_items`.

## Goals

- [ ] Create `definitions/schemas/search-item-v1.json` with the same fields as `movie-v1.json` and `tvshow-v1.json`.
- [ ] Create `definitions/resources/v1/search-tmdb.yml` defining `/v1/search`, query parameters `q` and `language`, `upstream` for `/search/multi`, and `upstream_items` for external IDs.
- [ ] Create parser `definitions/parsers/tmdb_search.py`.
- [ ] Add `fetch_tmdb_search` method to `UpstreamClient` in `it_mdb_api/services/upstream.py` supporting `upstream_items`.
- [ ] Update `it_mdb_api/worker.py` to process search queue tasks (`tasks:search`).
- [ ] Implement API endpoint in `it_mdb_api/api/v1/endpoints.py` for `/v1/search`.
- [ ] Add unit and integration tests for search parser, upstream client, worker, and endpoint.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Pagination across multiple search pages | Out of scope for initial v1 search endpoint implementation. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Schema structure | Identical to `movie-v1.json` / `tvshow-v1.json` with `media_type` | Requested by user. | y |
| Endpoint path | `/v1/search` | Requested by user. | y |
| Queue name | `tasks:search` | Keeps search tasks organized separately. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Search v1 Endpoint & Caching Flow ⭐ MVP

**User Story**: As an API consumer, I want to search for movies and TV shows using `/v1/search?q={query}&language={language}`, so that I can find content and view standardized details with external IDs.

**Acceptance Criteria**:

1. WHEN `definitions/schemas/search-item-v1.json` is inspected, THEN it SHALL have the same properties as movie/tvshow-v1 schemas plus `media_type`.
2. WHEN parser `tmdb_search.py` is executed with multi-search and external IDs results, THEN it SHALL return a list of standardized search items.
3. WHEN `GET /v1/search` is requested with `q`, THEN the API SHALL return cached search results or enqueue a task to fetch search results from TMDB using `upstream` and `upstream_items`.
4. All test suites in `tests/` SHALL pass successfully.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| SRCH-01 | P1 | Tasks | Pending |
| SRCH-02 | P1 | Tasks | Pending |
| SRCH-03 | P1 | Tasks | Pending |
| SRCH-04 | P1 | Tasks | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `ruff` passes with 0 errors.
