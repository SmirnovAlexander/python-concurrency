import multiprocessing
import random
import time
from multiprocessing import Process, Queue, RLock

from utils import logger


def task(lock):
    logger.info(f"Starting task!")
    for _ in range(5):
        lock.acquire()
        logger.info("Doing task!")

    for _ in range(5):
        lock.release()

    logger.info(f"Exiting task!")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    lock = RLock()

    lock.acquire()

    p1 = Process(target=task, args=(lock,))
    p2 = Process(target=task, args=(lock,))

    p1.start()
    p2.start()

    time.sleep(3)
    logger.info("Releasing lock!")
    lock.release()

    p1.join()
    p2.join()

    logger.info("Exiting!")
