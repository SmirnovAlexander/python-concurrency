import multiprocessing
import os
import time
from multiprocessing import Pool

from utils import logger


def init(pid: int):
    logger.info(f"Pool process with id {os.getpid()} received a task from main process {pid}")


def task(x: int) -> int:
    logger.info("Doing task!")
    return x * x


def on_success(result):
    logger.info(result)


def on_error(err):
    logger.info(err)


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    pid = os.getpid()
    pool = Pool(processes=1, initializer=init, initargs=(pid,), maxtasksperchild=1)

    result = pool.apply_async(task, args=(3,), callback=on_success, error_callback=on_error)

    time.sleep(3)
