import asyncio

import uvicorn
from fastapi import FastAPI
from loguru import logger
from utils import run_uvicorn_loguru

app = FastAPI()


@app.get("/")
async def read_root():
    logger.info("Received request...")
    await asyncio.sleep(10)
    return {"Hello": "World"}


if __name__ == "__main__":
    logger.info("Starting server...")
    run_uvicorn_loguru(uvicorn.Config("main:app", log_level="info", workers=1))
