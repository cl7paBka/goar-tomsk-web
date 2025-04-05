import asyncio
import uvicorn
import logging
from fastapi import FastAPI

from src.db.db import init_db
from src.api.routers import all_routers
from src.utils.config import settings

app = FastAPI(
    title="Goar-Cafe-API"
)

for router in all_routers:  # Include routers into FastAPI app from src/api/routes (all of them in src/api/routers.py)
    app.include_router(router)


async def main():
    logging.info("Starting init_db()")
    await init_db()

    logging.info("Starting FastAPI app")
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)


if __name__ == "__main__":
    asyncio.run(main())
