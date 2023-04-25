import time
from concurrent.futures import ThreadPoolExecutor

from utils import logger


def task(x):
    logger.info(f"Executing task with arg {x}")
    time.sleep(3)
    x = None
    return x * x


if __name__ == '__main__':

    executor = ThreadPoolExecutor()

    future = executor.submit(task, 10)

    logger.info(f"Is running: {future.running()}")
    logger.info(f"Is done: {future.done()}")
    logger.info(f"Attempt to cancel: {future.cancel()}")
    logger.info(f"Is cancelled: {future.cancelled()}")

    # res = future.result()
    # logger.info(res)
    ex = future.exception()
    logger.error(ex)

    logger.info("Exiting...")

    executor.shutdown()
