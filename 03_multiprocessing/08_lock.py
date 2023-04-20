import multiprocessing
import random
import time
from multiprocessing import Lock, Process, Queue

from utils import logger


def task(q, lock):
    logger.info(f"Starting task!")
    cnt = 0
    keep_running = True
    while keep_running:
        with lock:
            if not q.empty():
                logger.info(q.get())
                cnt += 1
            else:
                keep_running = False
        time.sleep(0.001)

    logger.info(f"Processed {cnt} items")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    q, l = Queue(), Lock()
    random.seed()
    for _ in range(100):
        q.put(random.randrange(10))

    consumer1 = Process(target=task, args=(q, l))
    consumer2 = Process(target=task, args=(q, l))

    consumer1.start()
    consumer2.start()

    consumer1.join()
    consumer2.join()
