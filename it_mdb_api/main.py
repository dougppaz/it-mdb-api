from fastapi import FastAPI

from it_mdb_api.api.v1.endpoints import router as v1_router

app = FastAPI(
    title="it-mdb-api",
    description="A cached, multi-language REST API for retrieving movie and TV show titles from IMDb and TMDB",
    version="0.1.0",
)

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
