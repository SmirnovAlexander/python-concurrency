import multiprocessing
import os
import random
import time
from multiprocessing import Pool, Queue

from utils import logger

random.seed()


def init(pid: int, q: Queue):
    task.q = q
    logger.info(f"Pool process with id {os.getpid()} received a task from main process {pid}")


def task(x: int) -> int:
    logger.info(f"Doing task {x}")
    tmp = x
    if random.randrange(5) == 0:
        logger.warning(f"Injecting failure!")
        tmp = None
    try:
        return tmp * tmp
    except:
        task.q.put(x)


if __name__ == "__main__":

    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    q = Queue()
    pool = Pool(processes=5, initializer=init, initargs=(os.getpid(), q), maxtasksperchild=None)

    target, result = range(11), []
    while target:
        partial_result = pool.map(task, iterable=target, chunksize=3)
        result.extend(partial_result)
        target = []
        while not q.empty():
            target.append(q.get())

    logger.info(result)
    logger.info("Exiting!")
