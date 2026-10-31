from fastapi import APIRouter, HTTPException, Query

from it_mdb_api.services.cache import CacheService
from it_mdb_api.services.queue import QueueService

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get("/movies/tt{imdb_id}")
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
    if cached_data is not None:
        return cached_data

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

        notified = await queue_service.wait_for_readiness(
            resource_key, timeout=timeout
        )
        if not notified:
            cached_data = await cache_service.get(resource_key)
            if cached_data is not None:
                return cached_data
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        if cached_data is not None:
            return cached_data

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get("/movies/{tmdb_id}")
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
    if cached_data is not None:
        return cached_data

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

        notified = await queue_service.wait_for_readiness(
            resource_key, timeout=timeout
        )
        if not notified:
            cached_data = await cache_service.get(resource_key)
            if cached_data is not None:
                return cached_data
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        if cached_data is not None:
            return cached_data

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get("/tvshows/tt{imdb_id}")
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
    if cached_data is not None:
        return cached_data

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

        notified = await queue_service.wait_for_readiness(
            resource_key, timeout=timeout
        )
        if not notified:
            cached_data = await cache_service.get(resource_key)
            if cached_data is not None:
                return cached_data
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        if cached_data is not None:
            return cached_data

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")


@router.get("/tvshows/{tmdb_id}")
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
    if cached_data is not None:
        return cached_data

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

        notified = await queue_service.wait_for_readiness(
            resource_key, timeout=timeout
        )
        if not notified:
            cached_data = await cache_service.get(resource_key)
            if cached_data is not None:
                return cached_data
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        cached_data = await cache_service.get(resource_key)
        if cached_data is not None:
            return cached_data

        raise HTTPException(status_code=504, detail="Gateway Timeout")

    except TimeoutError:
        raise HTTPException(status_code=504, detail="Gateway Timeout")
