# Add Movie v1 External IDs Specification

**Approved**: 2026-10-27 - user: "vamos so corrigir para que o imdb_id seja string.. e pode seguir pra implementacao. ambos campos novos podem ser nulos."

## Problem Statement

The `movie-v1` schema currently lacks explicit external provider identifiers (`imdb_id` and `tmdb_id`). When consumers request movie details via the TMDB endpoint `/v1/movies/{tmdb_id}`, both `imdb_id` and `tmdb_id` must be populated, fetching the IMDb identifier from TMDB's `/movie/{movie_id}/external_ids` endpoint.

## Goals

- [ ] Update `definitions/schemas/movie-v1.json` to include `imdb_id` (string) and `tmdb_id` (integer).
- [ ] Update `definitions/resources/v1/movies-tmdb.yml` to declare the upstream `external_ids` call alongside `movie`.
- [ ] Update `definitions/parsers/tmdb_movie.py` to populate `imdb_id` from external_ids and `tmdb_id` from movie ID.
- [ ] Update `definitions/parsers/imdb_movie.py` to populate `imdb_id` and set `tmdb_id` to null/None.
- [ ] Update `it_mdb_api/services/upstream.py` to invoke TMDB's `/movie/{movie_id}/external_ids` endpoint and pass its payload to the TMDB parser.
- [ ] Update unit and integration tests to verify `imdb_id` and `tmdb_id` are populated in responses.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| TMDB to IMDb bidirectional sync for IMDb endpoint | The `/v1/movies/tt{imdb_id}` endpoint does not query TMDB in this phase. |
| Additional external IDs (wikidata, facebook, instagram, twitter) | Only `imdb_id` and `tmdb_id` were requested for `movie-v1`. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| `imdb_id` field type | `["string", "null"]` | Standard IMDb alphanumeric identifier format starting with "tt", nullable if absent. | y |
| `tmdb_id` field type | `["integer", "null"]` | TMDB identifies movies using numeric integer IDs, nullable if absent. | y |
| Optionality of `imdb_id` and `tmdb_id` in schema | Optional and nullable | Some TMDB entries may lack IMDb IDs, and IMDb source does not populate `tmdb_id`. | y |
| Resilience when TMDB external_ids endpoint fails | Graceful fallback to empty external_ids | Upstream movie payload still returns valid movie details with `imdb_id: null`. | y |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: Add External IDs to Movie Schema, Resource, Parser and Upstream Client ⭐ MVP

**User Story**: As an API consumer calling `/v1/movies/{tmdb_id}`, I want the response to include `tmdb_id` and `imdb_id`, so that I can cross-reference movies across IMDb and TMDB.

**Acceptance Criteria**:

1. The `definitions/schemas/movie-v1.json` SHALL include `imdb_id` as string or null, and `tmdb_id` as integer or null in properties.
2. The `definitions/resources/v1/movies-tmdb.yml` SHALL include `external_ids` under `behavior.upstream` referencing `/movie/{tmdb_id}/external_ids`.
3. WHEN `tmdb_movie.py` parses input data with `movie` and `external_ids`, THEN the parser SHALL return a dictionary containing `tmdb_id` as an integer and `imdb_id` as a string.
4. WHEN `imdb_movie.py` parses input data with `movie`, THEN the parser SHALL return a dictionary containing `imdb_id` as a string and `tmdb_id` as null.
5. WHEN `UpstreamClient.fetch_tmdb_movie` is called, THEN the client SHALL request both the movie details and external_ids endpoints from TMDB API and pass both to the parser.
6. IF TMDB movie endpoint returns 404, THEN `UpstreamClient.fetch_tmdb_movie` SHALL raise `LookupError`.
7. WHEN endpoint `GET /v1/movies/{tmdb_id}` is invoked, THEN the system SHALL return movie details containing `tmdb_id` and `imdb_id`.
8. All test suites in `tests/` SHALL pass successfully with 100% pass rate.

**Independent Test**: Run `pytest` and verify tests for parsers, upstream client, and endpoints pass with `imdb_id` and `tmdb_id`.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| SCHEM-01 | P1 | Tasks | Pending |
| RES-01 | P1 | Tasks | Pending |
| PARS-01 | P1 | Tasks | Pending |
| UPSTR-01 | P1 | Tasks | Pending |
| TEST-01 | P1 | Tasks | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `validate_spec.py` passes with 0 errors.
- [ ] `ruff check it_mdb_api/ definitions/ tests/` passes with 0 errors.
