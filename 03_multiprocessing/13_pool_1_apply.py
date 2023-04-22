import multiprocessing
import os
from multiprocessing import Pool

from utils import logger


def init(pid: int):
    logger.info(f"Pool process with id {os.getpid()} received a task from main process {pid}")


def task(x: int) -> int:
    return x * x


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    pid = os.getpid()
    pool = Pool(processes=1, initializer=init, initargs=(pid,), maxtasksperchild=1)

    result = pool.apply(task, args=(3,))
    logger.info(result)
