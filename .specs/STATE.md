# Project State & Decision Log

## Decisions

| ID | Status | Decision | Rationale | Date |
| -- | ------ | -------- | --------- | - |
| AD-001 | active | Use Redis for cache, queue, and sync pub/sub | High performance, minimal resource overhead, native TTL and locking support. | 2023-10-13 |
| AD-002 | active | Default wait timeout of 30s with query string override (capped at 60s) | Balances user experience and upstream API responsiveness. | 2023-10-13 |
| AD-003 | active | Support `fakeredis` via environment variable (`USE_FAKE_REDIS=true`) for local development/testing | Enables robust local development and unit/integration testing without requiring an external Redis server. | 2023-10-24 |

## Handoff Snapshot

- **Current Feature**: `core-caching-queue`
- **Phase Completed**: Specify, Design, Tasks (all approved)
- **Next Step**: Execute Phase 3 (Task T4: Implement IMDb/TMDB External API Client & Parser)
