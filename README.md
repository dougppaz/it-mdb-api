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
| `APP_NAME` | Application name | `it-mdb-api` |
| `APP_ENV` | Application environment (`development`, `production`) | `development` |
| `APP_DEBUG` | Enable debug mode | `true` |
| `REDIS_URL` | Redis connection string for cache | `redis://localhost:6379/0` |
| `QUEUE_REDIS_URL` | Redis connection string for queue/background tasks | `redis://localhost:6379/1` |
| `USE_FAKE_REDIS` | Use in-memory `fakeredis` instead of real Redis (ideal for local testing) | `false` |
| `TMDB_API_READ_ACCESS_TOKEN` | TMDB API Read Access Token (Bearer token for upstream calls) | `""` |

---

## How to Run

### Standard Mode (Production / Real Redis)
Start the development server using Uvicorn via Poetry:
```bash
python3 -m poetry run uvicorn it_mdb_api.main:app --reload
```
And run the worker in a separate terminal:
```bash
python3 -m poetry run python3 -m it_mdb_api.worker
```

### Local Development with Unified Runner (`run.py`)
For local development and testing, you can run both the HTTP API server and the Background Worker concurrently in a **single Python process** using `run.py`:
```bash
python3 -m poetry run python3 run.py
```

> **⚠️ Important Notice on `run.py` & `fakeredis`:**
> `run.py` and `fakeredis` (`USE_FAKE_REDIS=true`) are designed **strictly for local development and testing**. Because `fakeredis` operates purely in-memory, running them in the same Python process allows the API and worker to share the same Redis state. **This solution must NOT be used in production environments**, where a standalone Redis instance/cluster and separate worker processes/containers are required.

### Running with Docker Compose

You can easily spin up the API, Worker, and a Redis instance using Docker. This setup automatically builds the production-ready Docker image with multi-stage builds.

1. Review and adjust environment variables in `.docker.env` if needed.
2. Run the services in detached mode:
   ```bash
   docker-compose up --build -d
   ```
3. Access the API on `http://localhost:8000`.

To view the logs from all services, run:
```bash
docker-compose logs -f
```

To shut down the services:
```bash
docker-compose down
```

---

## How to Test

Run the test suite using `pytest`:
```bash
python3 -m poetry run pytest
```
