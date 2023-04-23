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


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    pid = os.getpid()
    pool = Pool(processes=5, initializer=init, initargs=(pid,), maxtasksperchild=None)

    # it = pool.imap(task, iterable=range(11), chunksize=3)
    it = pool.imap_unordered(task, iterable=range(11), chunksize=3)

    for res in it:
        logger.info(res)

    logger.info("Exiting!")
