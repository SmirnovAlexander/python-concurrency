import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

from utils import logger


def task(arg):
    time.sleep(1)
    logger.info(f"Executing task {arg}")


if __name__ == '__main__':

    multiprocessing.set_start_method("spawn")

    executor = ProcessPoolExecutor()

    futures = []
    for i in range(10):
        futures.append(executor.submit(task, i))

    for future in futures:
        future.result()

    executor.shutdown()
