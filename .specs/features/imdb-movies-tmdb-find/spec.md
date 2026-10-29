# Implement IMDb Movies Endpoint via TMDB Find Specification

**Approved**: 2026-10-27 - user: "sim"

## Problem Statement

The API provides the resource contract `definitions/resources/v1/movies-imdb.yml` (`/v1/movies/tt{imdb_id}`) and parser `definitions/parsers/imdb_movie.py`, but has not implemented the upstream integration, endpoint route, or worker handling. We need to implement the IMDb movies endpoint using TMDB's `https://api.themoviedb.org/3/find/{external_id}` endpoint with `external_source=imdb_id`.

## Goals

- [ ] Update `definitions/resources/v1/movies-imdb.yml` to declare the upstream `find` call referencing TMDB v3 API find endpoint.
- [ ] Update `definitions/parsers/imdb_movie.py` to parse TMDB find output (`movie_results`) into `movie-v1` schema.
- [ ] Add `fetch_imdb_movie` to `it_mdb_api/services/upstream.py` calling `https://api.themoviedb.org/3/find/{external_id}?external_source=imdb_id`.
- [ ] Update `it_mdb_api/worker.py` to process tasks with `imdb_id`.
- [ ] Add `GET /v1/movies/tt{imdb_id}` route to `it_mdb_api/api/v1/endpoints.py`.
- [ ] Add unit and integration tests covering the IMDb endpoint, worker processing, and upstream client.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Non-movie results in find (TV, person) | Endpoint `/v1/movies/tt{imdb_id}` only handles movie results. |
| Other external sources in find (tvdb, wikidata) | Endpoint specifically queries by IMDb ID. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| TMDB find parameter `external_source` | `imdb_id` | Required query parameter by TMDB API to locate items by IMDb identifier. | y |
| IMDb movie not found condition | `movie_results` is empty or 404 | TMDB returns 200 with empty `movie_results` when the external ID is not found. | y |
| Path parameter format in route | `/movies/tt{imdb_id}` | Matches `movies-imdb.yml` spec and avoids collision with `/movies/{tmdb_id}`. | y |
| Cache key pattern | `movie:imdb:{imdb_id}:{language}` | Uses full IMDb ID (e.g. `movie:imdb:tt0137523:en`) conforming to resource spec. | y |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: Retrieve Movie Details by IMDb ID via TMDB Find ⭐ MVP

**User Story**: As an API consumer, I want to retrieve movie details using an IMDb ID via `/v1/movies/tt{imdb_id}` so that I can look up movies using their IMDb identifiers.

**Acceptance Criteria**:

1. The `definitions/resources/v1/movies-imdb.yml` SHALL include `find` under `behavior.upstream` referencing `/find/{imdb_id}` with `external_source: imdb_id`.
2. WHEN `imdb_movie.py` parses input data with `find` containing `movie_results`, THEN the parser SHALL return a dictionary conforming to `movie-v1` schema containing `imdb_id`, `tmdb_id`, and movie details.
3. WHEN `UpstreamClient.fetch_imdb_movie` is called with an IMDb ID, THEN the client SHALL request `https://api.themoviedb.org/3/find/{imdb_id}?external_source=imdb_id` from TMDB API.
4. IF TMDB find endpoint returns 404 or empty `movie_results`, THEN `UpstreamClient.fetch_imdb_movie` SHALL raise `LookupError`.
5. WHEN the worker receives a task payload with `imdb_id`, THEN the worker SHALL call `UpstreamClient.fetch_imdb_movie` and cache the result under `movie:imdb:{imdb_id}:{language}`.
6. WHEN a client calls `GET /v1/movies/tt{imdb_id}`, THEN the system SHALL return movie details containing `imdb_id`, `tmdb_id`, and `title`.
7. All test suites in `tests/` SHALL pass successfully with 100% pass rate.

**Independent Test**: Run `pytest` and verify tests for IMDb parser, upstream client find method, worker IMDb task handling, and `/v1/movies/tt{imdb_id}` endpoint pass successfully.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| RES-02 | P1 | Tasks | Pending |
| PARS-02 | P1 | Tasks | Pending |
| UPSTR-02 | P1 | Tasks | Pending |
| WORK-01 | P1 | Tasks | Pending |
| ROUTE-01 | P1 | Tasks | Pending |
| TEST-02 | P1 | Tasks | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `validate_spec.py` passes with 0 errors.
- [ ] `ruff check it_mdb_api/ definitions/ tests/` passes with 0 errors.
