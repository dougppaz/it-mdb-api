import asyncio
import json
import logging

from it_mdb_api.services.cache import CacheService
from it_mdb_api.services.queue import QueueService, get_queue_redis_client
from it_mdb_api.services.upstream import UpstreamClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("it-mdb-worker")


class Worker:
    def __init__(self, queue_name: str = "tasks:movies"):
        self.queue_name = queue_name
        self.cache_service = CacheService()
        self.queue_service = QueueService()
        self.upstream_client = UpstreamClient()
        self.running = False

    async def run(self):
        self.running = True
        logger.info("Worker started, listening on queue: %s", self.queue_name)
        client = get_queue_redis_client()

        while self.running:
            try:
                result = await client.blpop(self.queue_name, timeout=1)
                if not result:
                    continue

                _, raw_payload = result
                payload = json.loads(raw_payload)
                tmdb_id = payload.get("tmdb_id")
                imdb_id = payload.get("imdb_id")
                language = payload.get("language", "en-US")
                resource_key = payload.get("resource_key")

                if tmdb_id is not None:
                    logger.info(
                        "Processing task for TMDB movie ID: %s (lang: %s)",
                        tmdb_id,
                        language,
                    )
                else:
                    logger.info(
                        "Processing task for IMDb movie ID: %s (lang: %s)",
                        imdb_id,
                        language,
                    )

                try:
                    if tmdb_id is not None:
                        movie_data = await self.upstream_client.fetch_tmdb_movie(
                            tmdb_id, language=language
                        )
                    else:
                        movie_data = await self.upstream_client.fetch_imdb_movie(
                            imdb_id, language=language
                        )
                    await self.cache_service.set(
                        resource_key, movie_data, ttl=86400
                    )
                    await self.queue_service.publish_ready(resource_key)
                    logger.info(
                        "Successfully cached and notified for %s", resource_key
                    )
                except LookupError:
                    identifier = tmdb_id if tmdb_id is not None else imdb_id
                    logger.warning("Movie %s not found on upstream TMDB", identifier)
                    await self.cache_service.set(
                        resource_key, {"error": "Not found"}, ttl=300
                    )
                    await self.queue_service.publish_ready(resource_key)
                except Exception as e:  # noqa: BLE001
                    identifier = tmdb_id if tmdb_id is not None else imdb_id
                    logger.error("Error processing task for %s: %s", identifier, e)

            except asyncio.CancelledError:
                break
            except Exception as e:  # noqa: BLE001
                logger.error("Worker loop error: %s", e)
                await asyncio.sleep(1)

    def stop(self):
        self.running = False
        logger.info("Stopping worker...")


async def main():
    worker = Worker()
    try:
        await worker.run()
    except KeyboardInterrupt:
        worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
