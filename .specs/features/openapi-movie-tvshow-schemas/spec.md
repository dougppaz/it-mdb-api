# OpenAPI Movie and TVShow Response Schemas Specification

**Approved**: 2026-11-01 - user: "aprovado, pode criar as tarefas e seguir para implementacao"

## Problem Statement

Currently, the FastAPI endpoints (`/v1/movies/*` and `/v1/tvshows/*`) return raw dictionaries deserialized from Redis cache without Pydantic response models or return type annotations. As a result, FastAPI's automatically generated OpenAPI documentation (`/docs` and `/openapi.json`) does not specify or schema the response payloads for movies and TV shows, presenting them as generic objects.

## Goals

- [ ] Define Pydantic models (`MovieV1`, `TVShowV1`) matching the canonical JSON schemas (`definitions/schemas/movie-v1.json` and `definitions/schemas/tvshow-v1.json`).
- [ ] Annotate all movie and TV show FastAPI endpoints with `response_model` (`MovieV1` / `TVShowV1`).
- [ ] Ensure OpenAPI documentation correctly exposes movie and TV show response schemas.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Changing upstream API parsing logic | Out of scope; parsers already output matching data structures. |
| Modifying error response schemas | Out of scope; focus is strictly on successful movie and TV show response schemas. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Use Pydantic models for response serialization | Define `MovieV1` and `TVShowV1` matching JSON schemas | Ensures FastAPI integrates them into OpenAPI docs automatically | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: OpenAPI Response Schemas for Movies and TV Shows ⭐ MVP

**User Story**: As an API consumer or developer, I want the OpenAPI documentation to fully specify the response schemas for movie and TV show endpoints so that I can easily understand the payload structure and client libraries can be generated correctly.

**Why P1**: Essential for API usability, client SDK generation, and accurate OpenAPI documentation compliance.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHERE FastAPI OpenAPI documentation is accessed, the system SHALL expose schema definitions for `MovieV1` and `TVShowV1` entities. <!-- optional-feature -->
2. WHEN a client requests a movie via `/v1/movies/tt{imdb_id}` or `/v1/movies/{tmdb_id}`, the system SHALL validate and serialize the response against the `MovieV1` schema. <!-- event-driven -->
3. WHEN a client requests a TV show via `/v1/tvshows/tt{imdb_id}` or `/v1/tvshows/{tmdb_id}`, the system SHALL validate and serialize the response against the `TVShowV1` schema. <!-- event-driven -->
4. The system SHALL define `MovieV1` and `TVShowV1` models containing `id`, `title`, `original_title`, `year`, `overview`, `tmdb_poster_path`, `tmdb_backdrop_path`, `imdb_id`, and `tmdb_id` fields matching canonical JSON schemas. <!-- ubiquitous -->

**Independent Test**: Can verify by querying `/openapi.json` and checking that paths `/v1/movies/{tmdb_id}`, `/v1/movies/tt{imdb_id}`, `/v1/tvshows/{tmdb_id}`, and `/v1/tvshows/tt{imdb_id}` reference `MovieV1` and `TVShowV1` response schemas.

---

## Edge Cases

- IF optional fields (`original_title`, `year`, `overview`, `tmdb_poster_path`, `tmdb_backdrop_path`, `imdb_id`, `tmdb_id`) are `null` or missing in cached data, THEN system SHALL handle them gracefully as `None` in Pydantic models.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| OAPI-01 | P1: OpenAPI Response Schemas | Execute | Verified |
| OAPI-02 | P1: OpenAPI Response Schemas | Execute | Verified |
| OAPI-03 | P1: OpenAPI Response Schemas | Execute | Verified |
| OAPI-04 | P1: OpenAPI Response Schemas | Execute | Verified |

**ID format:** `[CATEGORY]-[NUMBER]`
**Status values:** Pending → In Design → In Tasks → Implementing → Verified

---

## Success Criteria

- [x] FastAPI `/openapi.json` successfully includes `MovieV1` and `TVShowV1` component schemas.
- [x] All 4 movie and TV show endpoints specify `response_model`.
- [x] Test suite passes successfully.
