import asyncio
import random
import time
from threading import Thread

from utils import logger


async def task(s: int):
    logger.info(f"Task started with arg {s}! Is event loop running = {asyncio.get_event_loop().is_running()}")
    await asyncio.sleep(s)
    logger.info("Task ending!")
    return 123


def launch_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task(random.randrange(5)))
    loop.close()


if __name__ == "__main__":

    logger.info("Starting program!")

    thread1 = Thread(target=launch_event_loop)
    thread2 = Thread(target=launch_event_loop)

    thread1.start()
    thread2.start()

    logger.info(f"Is event loop running = {asyncio.get_event_loop().is_running()}")

    thread1.join()
    thread2.join()
