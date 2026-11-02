from fastapi import APIRouter, HTTPException, Query

from it_mdb_api.schemas import MovieV1, SearchItemV1, TVShowV1
from it_mdb_api.services.cache import CacheService
from it_mdb_api.services.queue import QueueService

router = APIRouter(prefix="/v1", tags=["v1"])

ERROR_RESPONSES = {
    404: {"description": "Resource Not Found"},
    504: {"description": "Gateway Timeout"},
}


def _handle_cached_data(cached_data):
    if cached_data is not None:
        if isinstance(cached_data, dict) and cached_data.get("error") == "Not found":
            raise HTTPException(status_code=404, detail="Not found")
        return cached_data
    return None


@router.get(
    "/movies/tt{imdb_id}",
    response_model=MovieV1,
    response_model_exclude_none=True,
    responses=ERROR_RESPONSES,
)
async def get_imdb_movie(
    imdb_id: str,
    language: str = Query("en", description="Language code"),
    timeout: int = Query(
        30,
        ge=1,
        le=60,
        description="Max seconds to wait for cache population",
    ),
):
    resource_key = f"movie:imdb:tt{imdb_id}:{language}"
    cache_service = CacheService()
    queue_service = QueueService()

    # 1. Check cache
    cached_data = await cache_service.get(resource_key)
    res = _handle_cached_data(cached_data)
    if res is not None:
        return res

    # 2. Enqueue or wait
    task_payload = {
        "imdb_id": f"tt{imdb_id}",
        "language": language,
        "resource_key": resource_key,
    }
    queue_name = "tasks:movies"

    try:
        is_new = await queue_service.acquire_dedup_lock(
            resource_key, ttl=max(timeout * 2, 60)
        )
        if is_new:
            await queue_service.enqueue_task(queue_name, task_payload)

        notified = await queue_service.wait_for_readiness(resource_key, timeout=timeout)
        if not notified:
            cached_data = await cache_service.get(resource_key)
            res = _handle_cached_data(cached_data)
            if res is not None:
                return res
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        res = _handle_cached_data(cached_data)
        if res is not None:
            return res

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get(
    "/movies/{tmdb_id}",
    response_model=MovieV1,
    response_model_exclude_none=True,
    responses=ERROR_RESPONSES,
)
async def get_tmdb_movie(
    tmdb_id: int,
    language: str = Query("en-US", description="Language code"),
    timeout: int = Query(
        30,
        ge=1,
        le=60,
        description="Max seconds to wait for cache population",
    ),
):
    resource_key = f"movie:tmdb:{tmdb_id}:{language}"
    cache_service = CacheService()
    queue_service = QueueService()

    # 1. Check cache
    cached_data = await cache_service.get(resource_key)
    res = _handle_cached_data(cached_data)
    if res is not None:
        return res

    # 2. Enqueue or wait
    task_payload = {
        "tmdb_id": tmdb_id,
        "language": language,
        "resource_key": resource_key,
    }
    queue_name = "tasks:movies"

    try:
        is_new = await queue_service.acquire_dedup_lock(
            resource_key, ttl=max(timeout * 2, 60)
        )
        if is_new:
            await queue_service.enqueue_task(queue_name, task_payload)

        notified = await queue_service.wait_for_readiness(resource_key, timeout=timeout)
        if not notified:
            cached_data = await cache_service.get(resource_key)
            res = _handle_cached_data(cached_data)
            if res is not None:
                return res
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        res = _handle_cached_data(cached_data)
        if res is not None:
            return res

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get(
    "/tvshows/tt{imdb_id}",
    response_model=TVShowV1,
    response_model_exclude_none=True,
    responses=ERROR_RESPONSES,
)
async def get_imdb_tvshow(
    imdb_id: str,
    language: str = Query("en", description="Language code"),
    timeout: int = Query(
        30,
        ge=1,
        le=60,
        description="Max seconds to wait for cache population",
    ),
):
    resource_key = f"tvshow:imdb:tt{imdb_id}:{language}"
    cache_service = CacheService()
    queue_service = QueueService()

    cached_data = await cache_service.get(resource_key)
    res = _handle_cached_data(cached_data)
    if res is not None:
        return res

    task_payload = {
        "imdb_id": f"tt{imdb_id}",
        "language": language,
        "resource_key": resource_key,
        "resource_type": "tvshow",
    }
    queue_name = "tasks:tvshows"

    try:
        is_new = await queue_service.acquire_dedup_lock(
            resource_key, ttl=max(timeout * 2, 60)
        )
        if is_new:
            await queue_service.enqueue_task(queue_name, task_payload)

        notified = await queue_service.wait_for_readiness(resource_key, timeout=timeout)
        if not notified:
            cached_data = await cache_service.get(resource_key)
            res = _handle_cached_data(cached_data)
            if res is not None:
                return res
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        res = _handle_cached_data(cached_data)
        if res is not None:
            return res

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get(
    "/tvshows/{tmdb_id}",
    response_model=TVShowV1,
    response_model_exclude_none=True,
    responses=ERROR_RESPONSES,
)
async def get_tmdb_tvshow(
    tmdb_id: int,
    language: str = Query("en-US", description="Language code"),
    timeout: int = Query(
        30,
        ge=1,
        le=60,
        description="Max seconds to wait for cache population",
    ),
):
    resource_key = f"tvshow:tmdb:{tmdb_id}:{language}"
    cache_service = CacheService()
    queue_service = QueueService()

    cached_data = await cache_service.get(resource_key)
    res = _handle_cached_data(cached_data)
    if res is not None:
        return res

    task_payload = {
        "tmdb_id": tmdb_id,
        "language": language,
        "resource_key": resource_key,
        "resource_type": "tvshow",
    }
    queue_name = "tasks:tvshows"

    try:
        is_new = await queue_service.acquire_dedup_lock(
            resource_key, ttl=max(timeout * 2, 60)
        )
        if is_new:
            await queue_service.enqueue_task(queue_name, task_payload)

        notified = await queue_service.wait_for_readiness(resource_key, timeout=timeout)
        if not notified:
            cached_data = await cache_service.get(resource_key)
            res = _handle_cached_data(cached_data)
            if res is not None:
                return res
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        res = _handle_cached_data(cached_data)
        if res is not None:
            return res

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get(
    "/search",
    response_model=list[SearchItemV1],
    response_model_exclude_none=True,
    responses=ERROR_RESPONSES,
)
async def search_endpoint(
    q: str = Query(..., description="Search query string"),
    language: str = Query("en-US", description="Language code"),
    timeout: int = Query(
        30,
        ge=1,
        le=60,
        description="Max seconds to wait for cache population",
    ),
):
    resource_key = f"search:tmdb:{q}:{language}"
    cache_service = CacheService()
    queue_service = QueueService()

    # 1. Check cache
    cached_data = await cache_service.get(resource_key)
    res = _handle_cached_data(cached_data)
    if res is not None:
        return res

    # 2. Enqueue or wait
    task_payload = {
        "q": q,
        "language": language,
        "resource_key": resource_key,
        "resource_type": "search",
    }
    queue_name = "tasks:search"

    try:
        is_new = await queue_service.acquire_dedup_lock(
            resource_key, ttl=max(timeout * 2, 60)
        )
        if is_new:
            await queue_service.enqueue_task(queue_name, task_payload)

        notified = await queue_service.wait_for_readiness(resource_key, timeout=timeout)
        if not notified:
            cached_data = await cache_service.get(resource_key)
            res = _handle_cached_data(cached_data)
            if res is not None:
                return res
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        res = _handle_cached_data(cached_data)
        if res is not None:
            return res

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")
