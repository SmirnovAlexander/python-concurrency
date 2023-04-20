import multiprocessing
import time
from multiprocessing import Process, Queue, Semaphore, Value

from utils import logger


def task(val, sem1, sem2):
    logger.info(f"Starting task!")
    logger.info(f"Received {val} (id {id(val)})")
    sem1.release()
    sem2.acquire()
    logger.info(f"After change: {val} (id {id(val)})")
    logger.info(f"Finished task!")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    q = Queue()
    sem1, sem2 = Semaphore(0), Semaphore(0)

    val = Value('i', 228)
    logger.info(f"Initialized object (id {id(val)})")

    process = Process(target=task, args=(val, sem1, sem2))
    process.start()

    time.sleep(1)
    q.put(val)
    sem1.acquire()

    val.value += 322
    logger.info("Changed value!")

    sem2.release()

    logger.info("Exiting!")
