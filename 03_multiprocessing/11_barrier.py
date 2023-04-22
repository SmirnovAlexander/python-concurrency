import random
import time
from multiprocessing import Barrier, Process

from utils import logger


def task():
    time.sleep(random.randint(1, 8))
    logger.info(f"{barrier.n_waiting} processes blocked on barrier!")
    barrier.wait()


def on_exit():
    logger.info(f"{barrier.n_waiting} processes came. Barrier is gone!")


if __name__ == "__main__":

    n_processes = 5
    barrier = Barrier(n_processes, action=on_exit)

    processes = [Process(target=task) for _ in range(n_processes)]
    for i in range(n_processes):
        processes[i].start()

    # logger.info("Aborting barrer")
    # barrier.abort()

    logger.info("Exiting!")
