# it-mdb-api

A cached, multi-language REST API for retrieving movie and TV show titles from IMDb and TMDB with async queue processing and request coalescing.

---

## Prerequisites

- **Python** (managed via [asdf-vm](https://asdf-vm.com/): check `.tool-versions`)
- **Poetry** (package manager)
- **Redis** (optional if using `fakeredis` for local development/testing)

---

## Installation

1. Install dependencies using Poetry:
   ```bash
   python3 -m poetry install
   ```

2. Configure environment variables (create a `.env` file or export them):
   ```bash
   cp .env.example .env
   ```

---

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `USE_FAKE_REDIS` | Use in-memory `fakeredis` instead of real Redis (ideal for local testing) | `false` |
| `TMDB_API_READ_ACCESS_TOKEN` | TMDB API Read Access Token (Bearer token for upstream calls) | `""` |
| `APP_ENV` | Application environment (`development`, `production`) | `development` |
| `APP_DEBUG` | Enable debug mode | `true` |

---

## How to Run

Start the development server using Uvicorn via Poetry:
```bash
python3 -m poetry run uvicorn it_mdb_api.main:app --reload
```

---

## How to Test

Run the test suite using `pytest`:
```bash
python3 -m poetry run pytest
```
