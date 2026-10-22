# Core Caching and Async Queue Architecture Specification

## Problem Statement

The API needs to fetch movie and TV show data, search results, and cross-reference IDs between IMDb and TMDB efficiently without hammering external APIs or wasting compute resources. Without a unified caching and async queue mechanism, concurrent requests for uncached resources cause duplicate upstream requests, high latency, and high resource utilization.

## Goals

- [ ] Implement a unified, generic caching and queueing flow for all resources (movies, TV shows, search, ID mappings).
- [ ] Ensure cache-first retrieval with zero external API calls on cache hits.
- [ ] Prevent duplicate queue items when multiple requests arrive for the same uncached resource (deduplication / request coalescing / listening to existing queue task).
- [ ] Allow incoming requests for uncached resources to wait for cache population up to a configurable timeout (default 30 seconds, customizable via query string).
- [ ] Utilize Redis (or equivalent lightweight data store) for caching, queue management, and synchronization to minimize resource usage.

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
| ------- | ------ |
| Frontend UI | This is a backend REST API project. |
| Persistent relational database storage (PostgreSQL/MySQL) | Caching and transient queue state in Redis are sufficient for this phase; long-term data persistence beyond cache is out of scope unless explicitly requested. |

---

## Assumptions & Open Questions

Every ambiguity is resolved or recorded here - nothing is left silently unclear.

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --------------------- | -------------- | --------- | ---------- |
| Redis as backing store | Redis for cache, queue, and pub/sub or polling synchronization | Highly efficient, minimal resource usage, native support for TTL and pub/sub. | y |
| Default timeout | 30 seconds, overrideable via `timeout` query parameter (capped at max 60s) | Balances user experience with upstream API latency limits. | y |
| Queue worker architecture | Background worker pool consuming from Redis queue | Decouples HTTP request lifecycle from external API calls. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Generic Cache-First Retrieval & Async Queue Wait ⭐ MVP

**User Story**: As an API client, I want to request any resource (movie, TV show, search, ID mapping) and receive cached data instantly, or wait while a background worker fetches and caches it if missing, so that I get fast responses without duplicate upstream requests.

**Why P1**: This is the core engine of the entire API. Every endpoint depends on this flow.

**Acceptance Criteria** (each line is one EARS pattern):

1. WHEN a request is made for a resource whose data exists in the cache, the system SHALL return the cached data immediately with HTTP 200 without calling external APIs. <!-- event-driven -->
2. WHEN a request is made for a resource whose data is not in the cache and not currently in the queue, the system SHALL enqueue a job for the resource, and the request SHALL wait for the cache to be populated up to the specified timeout (default 30 seconds, or overridden via query parameter). <!-- event-driven -->
3. WHEN a request is made for a resource whose data is not in the cache but is already present in the queue/processing, the system SHALL NOT create a duplicate queue item, and SHALL wait for the existing processing to populate the cache. <!-- event-driven -->
4. IF the timeout is reached while waiting for an uncached resource to be processed, THEN the system SHALL return an HTTP 504 Gateway Timeout response. <!-- unwanted-behavior -->
5. WHILE a resource request is waiting for cache population, the system SHALL periodically check or subscribe to cache/queue readiness notifications. <!-- state-driven -->
6. The system SHALL support customizing the wait timeout via query string parameter `timeout` (e.g. `?timeout=15`), with a maximum allowed cap of 60 seconds. <!-- ubiquitous -->

**Independent Test**: Can demo by requesting an uncached ID, observing that a single job is queued, concurrent requests wait for the same job, and once processed, all requests receive the cached payload successfully.

---

## Edge Cases

Edge cases are usually unwanted-behavior (IF/THEN) or boundary (WHEN) criteria:

- IF the external upstream API (IMDb/TMDB) returns a 404 Not Found, THEN the system SHALL cache a negative result / 404 state for a short TTL and return HTTP 404 to all waiting clients.
- IF the external upstream API fails or times out during worker processing, THEN the system SHALL mark the queue task as failed, release locks, and return HTTP 502 to waiting clients.
- WHEN an invalid `timeout` query parameter (non-integer, negative) is provided, THEN the system SHALL fall back to the default 30-second timeout.

---

## Requirement Traceability

Each requirement gets a unique ID for tracking across design, tasks, and validation.

| Requirement ID | Story | Phase | Status |
| -------------- | ----- | ----- | ------ |
| CORE-01 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |
| CORE-02 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |
| CORE-03 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |
| CORE-04 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |
| CORE-05 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |
| CORE-06 | P1: Generic Cache-First Retrieval & Async Queue Wait | Tasks | In Tasks |

**ID format:** `[CATEGORY]-[NUMBER]` (e.g., `CORE-01`)

**Status values:** Pending → In Design → In Tasks → Implementing → Verified

**Coverage:** 6 total, 6 mapped to tasks, 0 unmapped

---

## Success Criteria

How we know the feature is successful:

- [ ] Uncached requests successfully queue and wait for worker completion without duplicate queue entries.
- [ ] Cache hits return instantly without upstream calls.
- [ ] Timeout query parameter correctly bounds waiting requests.
