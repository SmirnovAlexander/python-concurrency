import multiprocessing
import os
import time
from multiprocessing import Pool

from utils import logger


def init(pid: int):
    logger.info(f"Pool process with id {os.getpid()} received a task from main process {pid}")


def task(x: int) -> int:
    logger.info(f"Doing task {x}!")
    return x * x


def on_success(result):
    logger.info(result)


def on_error(err):
    logger.info(err)


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    pid = os.getpid()
    pool = Pool(processes=5, initializer=init, initargs=(pid,), maxtasksperchild=None)

    promise = pool.map_async(task, iterable=range(11), chunksize=3, callback=on_success, error_callback=on_error)
    # result = promise.get()
    # logger.info(result)

    pool.close()
    pool.join()

    logger.info("Exiting!")
