# API Definitions - README

This directory (`definitions/`) contains custom YAML endpoint specifications, JSON schemas, Python parser scripts, and upstream service definitions for `it-mdb-api`.

---

## Structure

```
definitions/
├── README.md
├── schemas/
│   └── movie-v1.json
├── parsers/
│   ├── imdb_movie.py
│   └── tmdb_movie.py
├── upstream/
│   └── tmdb-v3-api.yml
└── resources/
    └── v1/
        ├── movies-imdb.yml
        └── movies-tmdb.yml
```

---

## Upstream Service Definitions (`upstream/*.yml`)

Upstream service definitions model external APIs, centralizing base URLs, shared authentication, and rate-limiting policies:

| Field | Type | Description |
| --- | --- | --- |
| `name` | `string` | Service identifier. |
| `base_url` | `string` | Root URL for the upstream service. |
| `authentication.type` | `string` | Auth type (`bearer`, `api_key`, etc.). |
| `authentication.location` | `string` | Where auth is placed (`header`, `query`, etc.). |
| `authentication.name` | `string` | Header or query parameter name. |
| `authentication.env_var` | `string` | Environment variable name storing the secret credential. |
| `rate_limit.requests_per_second` | `integer` | Rate limit threshold per second. |
| `rate_limit.burst` | `integer` | Allowed burst capacity. |

---

## Resource Definition Schema Guide (`resources/v1/*.yml`)

Each resource definition file defines a `GET` endpoint and maps to a response JSON schema, a parser script, and upstream service invocation details:

| Field | Type | Description |
| --- | --- | --- |
| `schema` | `string` | Relative path to the JSON Schema validating output (e.g. `definitions/schemas/movie-v1.json`). |
| `source` | `string` | Upstream data provider (`imdb`, `tmdb`). |
| `endpoint` | `string` | REST API URL path template. |
| `description` | `string` | Brief description of the endpoint. |
| `parameters.path` | `list` | Path parameters required by the endpoint. |
| `parameters.query` | `list` | Resource-specific query parameters (e.g., `language`). |
| `behavior.cache.key_pattern` | `string` | Redis cache key template (e.g. `movie:tmdb:{tmdb_id}:{language}`). |
| `behavior.cache.ttl_seconds` | `integer` | Cache TTL in seconds for successful responses. |
| `behavior.cache.negative_ttl_seconds` | `integer` (optional) | TTL for negative/404 responses. |
| `behavior.parser` | `string` | Relative path to parser script (`definitions/parsers/[name].py`). |
| `behavior.upstream` | `map` | Dictionary of upstream service invocation details keyed by request name (enabling multiple requests). |
| `behavior.upstream.[key].modality` | `string` | Path to upstream service definition (`definitions/upstream/tmdb-v3-api.yml`). |
| `behavior.upstream.[key].method` | `string` | HTTP method (`GET`, etc.). |
| `behavior.upstream.[key].path` | `string` | Upstream relative path template (e.g. `/movie/{tmdb_id}`). |
| `behavior.upstream.[key].query_params` | `map` | Query parameters sent to the upstream service. |

> **Note on Shared Elements:**
> - All endpoints are `GET`.
> - Global query parameters (such as `?timeout=30`) and HTTP status code behaviors (200, 404, 504) are handled globally across all resource endpoints.

---

## Parser Scripts (`parsers/[name].py`)

Each parser script receives a raw JSON input file path via command-line argument, parses it, and outputs the standardized dictionary as JSON on stdout.

**Contract:**
- Must expose a function `parse(input_data: dict) -> dict`. `input_data` is a dictionary where upstream call results are named (keyed by upstream request names, e.g. `{"movie": {...}}`).
- CLI execution: `python3 definitions/parsers/[name].py <input_json_file>` -> prints JSON output.
