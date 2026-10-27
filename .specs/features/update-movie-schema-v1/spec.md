# Update Movie Schema v1 Specification

**Approved**: 2025-05-18 - user: "vamos ajustar o schema de movie-v1: remova o campo genres e rating. adicione os campos tmdb_poster_path e tmdb_backdrop_path."

## Problem Statement

The `movie-v1` schema currently includes `genres` and `rating`, but lacks poster and backdrop image paths from TMDB (`tmdb_poster_path` and `tmdb_backdrop_path`). We need to update the schema, parsers, and tests to reflect this change.

## Goals

- [ ] Update `definitions/schemas/movie-v1.json` to remove `genres` and `rating`, and add `tmdb_poster_path` and `tmdb_backdrop_path`.
- [ ] Update `definitions/parsers/tmdb_movie.py` to parse `poster_path` and `backdrop_path` into `tmdb_poster_path` and `tmdb_backdrop_path`, and remove `genres` and `rating`.
- [ ] Update `definitions/parsers/imdb_movie.py` to remove `genres` and `rating`, setting `tmdb_poster_path` and `tmdb_backdrop_path` to `None`.
- [ ] Update all corresponding tests and test mocks in `tests/`.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| IMDb poster/backdrop scraping | IMDb upstream does not provide poster/backdrop paths in this scope. |
| Other movie schema versions | Only `movie-v1` schema is affected. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
|---------------------|---------------|---------|----------|
| `tmdb_poster_path` and `tmdb_backdrop_path` types | `string` (or null) | Standard TMDB image path strings (e.g. `/path.jpg`) | y |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: Update Movie Schema and Parsers ⭐ MVP

**User Story**: As an API consumer, I want movie responses to include TMDB poster and backdrop paths instead of genres and ratings, so that the movie representation matches the current UI/client requirements.

**Acceptance Criteria**:

1. The `definitions/schemas/movie-v1.json` SHALL not contain `genres` or `rating` properties.
2. The `definitions/schemas/movie-v1.json` SHALL include `tmdb_poster_path` and `tmdb_backdrop_path` properties of type string (or nullable).
3. WHEN `tmdb_movie.py` parses TMDB input data, THEN the output dictionary SHALL contain `tmdb_poster_path` and `tmdb_backdrop_path` and SHALL NOT contain `genres` or `rating`.
4. WHEN `imdb_movie.py` parses IMDb input data, THEN the output dictionary SHALL NOT contain `genres` or `rating` and SHALL have `tmdb_poster_path` and `tmdb_backdrop_path` as null/None.
5. All test suites in `tests/` SHALL pass successfully with the updated schema and parsers.

**Independent Test**: Run `pytest` and verify all unit and integration tests pass successfully.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| -------------- | ----- | ----- | ------ |
| SCHEM-01 | P1 | Execute | Pending |
| PARS-01 | P1 | Execute | Pending |
| TEST-01 | P1 | Execute | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `validate_spec.py` passes successfully.
