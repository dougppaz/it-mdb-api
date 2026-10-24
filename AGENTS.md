# AGENTS.md - Instructions for AI Coding Agents on it-mdb-api

## Core Standards & Workflow
- **Skill**: Follow the `tlc-spec-driven` skill lifecycle (Specify → Design → Tasks → Execute → Validate).
- **Tooling**:
  - Python via `asdf-vm` (`.tool-versions`).
  - Package management via Poetry using **`python3 -m poetry [...]`**.
  - Test runner: `pytest`. Linter/formatter: `ruff`.
- **Source of Truth for Contracts**: The `definitions/` directory contains YAML specs, JSON schemas (`definitions/schemas/`), parser scripts (`definitions/parsers/`), and upstream service definitions (`definitions/upstream/`). Use them as documentation contracts.
- **Configuration Rule**: Always import and consume the centralized `settings` singleton instance (`from it_mdb_api.settings import settings`) instead of instantiating configuration classes directly (e.g., never call `RedisSettings()`).
- **Commits**: One atomic Conventional Commit per task, updated in `tasks.md` before committing.
