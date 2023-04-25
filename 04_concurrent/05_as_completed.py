import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

from utils import logger


def task(x: int) -> int:
    logger.info(f"Doing task with arg {x}")
    time.sleep(10 - x)
    logger.info(f"Finished task with arg {x}")
    return x * x


if __name__ == "__main__":

    thread_executor = ThreadPoolExecutor()
    process_executor = ProcessPoolExecutor()

    futures = []

    futures.extend([thread_executor.submit(task, i) for i in range(5)])
    futures.extend([process_executor.submit(task, i) for i in range(5, 10)])

    # res = as_completed(futures, timeout=None)
    res = as_completed(futures, timeout=3)

    for future in res:
        logger.info(future.result())

    thread_executor.shutdown(wait=False)
    process_executor.shutdown(wait=False)

    logger.info("Exiting...")
