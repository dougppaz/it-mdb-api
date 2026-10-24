import os

import pytest

from it_mdb_api.services.cache import CacheService, get_redis_client


@pytest.fixture(autouse=True)
def set_fake_redis():
    os.environ["USE_FAKE_REDIS"] = "true"
    yield
    os.environ.pop("USE_FAKE_REDIS", None)

@pytest.mark.asyncio
async def test_cache_set_and_get():
    client = get_redis_client()
    service = CacheService(client)
    
    await service.set("test:key", {"foo": "bar"}, ttl=60)
    val = await service.get("test:key")
    assert val == {"foo": "bar"}

@pytest.mark.asyncio
async def test_cache_get_missing():
    service = CacheService()
    val = await service.get("missing:key")
    assert val is None

@pytest.mark.asyncio
async def test_cache_set_nx():
    service = CacheService()
    success1 = await service.set_nx("lock:key", "locked", ttl=10)
    assert success1 is True
    
    success2 = await service.set_nx("lock:key", "locked-again", ttl=10)
    assert success2 is False
