import time
from concurrent.futures import ThreadPoolExecutor

from utils import logger


def task(x):
    logger.info(f"Executing task with arg {x}")
    if x == 5:
        time.sleep(10)
    return x * x


if __name__ == '__main__':

    executor = ThreadPoolExecutor()

    it = executor.map(task, range(10), timeout=2)

    for res in it:
        logger.info(res)

    executor.shutdown()
