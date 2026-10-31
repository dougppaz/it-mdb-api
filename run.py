import asyncio
import uvicorn

from it_mdb_api.main import app
from it_mdb_api.worker import Worker


async def run_server():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def run_worker():
    worker = Worker(queue_name=["tasks:movies", "tasks:tvshows"])
    await worker.run()


async def main():
    print("=" * 70)
    print("Starting it-mdb-api HTTP Server & Worker in a Single Python Process")
    print("Sharing in-memory Fakeredis across API requests and background worker.")
    print("=" * 70)
    await asyncio.gather(run_server(), run_worker())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down local runner...")
