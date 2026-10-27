# Project State & Decision Log

## Decisions

| ID | Status | Decision | Rationale | Date |
| -- | ------ | -------- | --------- | - |
| AD-001 | active | Use Redis for cache, queue, and sync pub/sub | High performance, minimal resource overhead, native TTL and locking support. | 2023-10-13 |
| AD-002 | active | Default wait timeout of 30s with query string override (capped at 60s) | Balances user experience and upstream API responsiveness. | 2023-10-13 |
| AD-003 | active | Support `fakeredis` via environment variable (`USE_FAKE_REDIS=true`) for local development/testing | Enables robust local development and unit/integration testing without requiring an external Redis server. | 2023-10-24 |

## Handoff Snapshot

- **Current Feature**: `add-movie-v1-external-ids`
- **Phase Completed**: Specify, Tasks (both approved)
- **Next Step**: Execute tasks T1 -> T9.
