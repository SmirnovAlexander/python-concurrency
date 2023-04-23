import multiprocessing
import os
import time
from multiprocessing import Pool

from utils import logger


def init(pid: int):
    logger.info(f"Pool process with id {os.getpid()} received a task from main process {pid}")


def task(x: int, chunk_name: str) -> int:
    logger.info(f"Doing {chunk_name}!")
    return x * x


def on_success(result):
    logger.info(result)


def on_error(err):
    logger.error(err)


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    pid = os.getpid()
    pool = Pool(processes=5, initializer=init, initargs=(pid,), maxtasksperchild=None)

    promise = pool.starmap_async(
        task, iterable=[(i, f"item-{i}") for i in range(11)], chunksize=3, callback=on_success, error_callback=on_error
    )
    # result = promise.get()
    # logger.info(result)

    pool.close()
    pool.join()

    logger.info("Exiting!")
