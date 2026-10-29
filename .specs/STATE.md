# Project State & Decision Log

## Decisions

| ID | Status | Decision | Rationale | Date |
| -- | ------ | -------- | --------- | - |
| AD-001 | active | Use Redis for cache, queue, and sync pub/sub | High performance, minimal resource overhead, native TTL and locking support. | 2023-10-13 |
| AD-002 | active | Default wait timeout of 30s with query string override (capped at 60s) | Balances user experience and upstream API responsiveness. | 2023-10-13 |
| AD-003 | active | Support `fakeredis` via environment variable (`USE_FAKE_REDIS=true`) for local development/testing | Enables robust local development and unit/integration testing without requiring an external Redis server. | 2023-10-24 |
| AD-004 | active | Add nullable `imdb_id` and `tmdb_id` to movie-v1 schema | Supports cross-referencing between TMDB and IMDb via TMDB external_ids endpoint. | 2026-10-27 |
| AD-005 | active | Implement IMDb movies endpoint using TMDB Find API (`/find/{imdb_id}`) | Allows looking up movies by IMDb ID via TMDB's Find service, ensuring consistent data schema. | 2026-10-27 |

## Handoff Snapshot

- **Current Feature**: `imdb-movies-tmdb-find`
- **Phase Completed**: Specify, Tasks, Execute, Verify (all passed)
- **Next Step**: Feature complete and verified. Ready for next instructions.
