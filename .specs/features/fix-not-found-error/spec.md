# Fix 500 Error on Not Found Resources Specification

**Approved**: 2025-11-02 - user: "crie a especificacao baseado na solucao ou implementando ferramentas para melhor investigacao"

## Problem Statement

When an upstream resource (movie or TV show) is not found on TMDB (`LookupError`), the worker caches `{"error": "Not found"}` with a TTL of 300 seconds. When API endpoints retrieve this cached error object, FastAPI attempts to validate it against `MovieV1` or `TVShowV1` response models, causing a `ResponseValidationError` resulting in HTTP 500 Internal Server Error instead of HTTP 404 Not Found (as seen in `error.log.txt`).

## Goals

- [ ] Update API endpoints (`/v1/movies/...`, `/v1/tvshows/...`) in `it_mdb_api/api/v1/endpoints.py` to check if cached data contains `{"error": "Not found"}` and raise `HTTPException(status_code=404, detail="Not found")`.
- [ ] Add integration tests verifying that requesting non-existent movies and TV shows correctly returns HTTP 404 Not Found.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| --- | --- |
| Changing worker cache error payload structure | `{"error": "Not found"}` is standard; handling it at the API endpoint layer is robust and stack-appropriate. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Error detection in cache | Check `isinstance(cached_data, dict) and cached_data.get("error") == "Not found"` | Matches worker error caching pattern (`{"error": "Not found"}`). | y |
| HTTP Status code for not found | 404 Not Found | Correct REST semantic response for missing resources. | y |

**Open questions:** none - all resolved or logged above (required before the spec is confirmed).

---

## User Stories

### P1: Return 404 Not Found for Missing Resources ⭐ MVP

**User Story**: As an API consumer, I want requests for non-existent movies or TV shows to return HTTP 404 Not Found instead of HTTP 500 Internal Server Error, so that error handling is correct and predictable.

**Acceptance Criteria**:

1. **WHEN** an API endpoint retrieves cached data indicating `{"error": "Not found"}`, **THEN** the system **SHALL** raise an `HTTPException` with status code 404 and detail `"Not found"`.
2. **WHEN** a client requests a movie or TV show ID that does not exist on upstream (resulting in cached `{"error": "Not found"}`), **THEN** the response **SHALL** return HTTP 404 Not Found.
3. All test suites in `tests/` **SHALL** pass successfully.

**Independent Test**: Run `pytest` and verify tests for movie and TV show 404 responses pass successfully.

---

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| ERR-01 | P1 | Execute | Pending |
| TEST-01 | P1 | Execute | Pending |

## Success Criteria

- [ ] `pytest` passes with 100% success.
- [ ] `validate_spec.py fix-not-found-error` passes with 0 errors.
- [ ] `ruff check it_mdb_api/ definitions/ tests/` passes with 0 errors.

## Checks

**C1** - API endpoints return 404 when cached data contains `{"error": "Not found"}` (ERR-01, AC 1, AC 2)
Proof: `pytest tests/integration/test_endpoints.py -k "not_found"`
