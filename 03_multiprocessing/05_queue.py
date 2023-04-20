import multiprocessing
import random
from multiprocessing import Process, Queue

from utils import logger


def task(q):
    logger.info(f"Starting task!")
    cnt = 0
    while not q.empty():
        # hangs because when one elem left it
        # gets blocked by one of processes
        # logger.info(q.get())
        try:
            logger.info(q.get(block=False, timeout=5))
            cnt += 1
        except:
            pass
    logger.info(f"Processed {cnt} items")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    q = Queue()
    q.get
    random.seed()
    for _ in range(100):
        q.put(random.randrange(10))

    consumer1 = Process(target=task, args=(q,))
    consumer2 = Process(target=task, args=(q,))

    consumer1.start()
    consumer2.start()

    consumer1.join()
    consumer2.join()
