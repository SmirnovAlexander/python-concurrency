import asyncio
from functools import lru_cache

import uvicorn
from async_lru import alru_cache
from fastapi import FastAPI
from loguru import logger
from utils import run_uvicorn_loguru

app = FastAPI()


# @lru_cache
# @alru_cache
async def long_task():
    await asyncio.sleep(3)
    return {"Hello": "World"}


@app.get("/")
@alru_cache
async def read_root():
    logger.info("Received request...")
    return await long_task()


if __name__ == "__main__":
    logger.info("Starting server...")
    run_uvicorn_loguru(uvicorn.Config("main:app", log_level="info", workers=1))
