import asyncio
import random
import time
from asyncio import Future
from threading import Thread, current_thread

from utils import logger

shutdown = False


async def resolver(future):
    logger.info(f"If event loop is running: {asyncio.get_event_loop().is_running()}")
    await asyncio.sleep(5)
    future.set_result(None)


async def monitor_coro():
    global shutdown

    while shutdown == False:
        logger.info("Alive at {0}".format(time.time()))
        await asyncio.sleep(1)


async def coro():
    global shutdown

    logger.info("Coroutine running!")
    future = Future()
    loop = asyncio.get_event_loop()

    monitor_coro_future = asyncio.ensure_future(monitor_coro())
    resolver_future = asyncio.ensure_future(resolver(future))

    logger.info(f"If event loop is running: {asyncio.get_event_loop().is_running()}")

    await future
    await asyncio.sleep(2)
    shutdown = True
    logger.info("coro exiting")

    await monitor_coro_future, resolver_future


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    logger.info(f"If event loop is running: {asyncio.get_event_loop().is_running()}")

    loop.run_until_complete(coro())
    logger.info("main exiting")
