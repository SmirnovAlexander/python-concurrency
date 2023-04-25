import time
from concurrent.futures import ThreadPoolExecutor

from utils import logger


def task(x):
    logger.info(f"Executing task with arg {x}")
    time.sleep(3)
    logger.info(x * x)


if __name__ == '__main__':

    executor = ThreadPoolExecutor(max_workers=1)

    future1 = executor.submit(task, 10)
    future2 = executor.submit(task, 20)

    logger.info(f"1 Is running: {future1.running()}")
    logger.info(f"1 Is done: {future1.done()}")
    logger.info(f"1 Attempt to cancel: {future1.cancel()}")
    logger.info(f"1 Is cancelled: {future1.cancelled()}")

    logger.info(f"2 Is running: {future2.running()}")
    logger.info(f"2 Is done: {future2.done()}")
    logger.info(f"2 Attempt to cancel: {future2.cancel()}")
    logger.info(f"2 Is cancelled: {future2.cancelled()}")

    logger.info("Exiting...")

    executor.shutdown()
