import asyncio
import time

from utils import logger


async def task():
    logger.info("Task started!")
    await asyncio.sleep(5)
    logger.info("Task ending!")
    return 123


if __name__ == "__main__":

    logger.info("Starting program!")
    res = asyncio.run(task())
    logger.info(res)
