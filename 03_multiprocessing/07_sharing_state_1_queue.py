import multiprocessing
import time
from multiprocessing import Process, Queue, Semaphore

from utils import logger


def task(q, sem1, sem2):
    logger.info(f"Starting task!")
    val = q.get()
    logger.info(f"Received {val}")
    sem1.release()
    sem2.acquire()
    logger.info(f"After change: {val}")
    logger.info(f"Finished task!")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    q = Queue()
    sem1, sem2 = Semaphore(0), Semaphore(0)

    val = 228

    process = Process(target=task, args=(q, sem1, sem2))
    process.start()

    time.sleep(1)
    q.put(val)
    sem1.acquire()

    val = 322
    logger.info("Changed value!")

    sem2.release()

    logger.info("Exiting!")
