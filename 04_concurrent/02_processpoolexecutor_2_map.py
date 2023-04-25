import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

from utils import logger


def task(x):
    logger.info(f"Executing task with arg {x}")
    if x == 5:
        time.sleep(10)
    return x * x


if __name__ == '__main__':

    multiprocessing.set_start_method("fork")

    executor = ProcessPoolExecutor()

    it = executor.map(task, range(10))

    for res in it:
        logger.info(res)

    executor.shutdown()
