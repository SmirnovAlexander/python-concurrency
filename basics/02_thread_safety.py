import dis
import threading
from loguru import logger
from threading import Lock

# count = 0
# def increment():
#     global count
#     count += 1
# dis.dis(increment)

TARGET_SUM = 1_000_000
N_THREADS = 5

class Counter:

    def __init__(self):
        self.cnt = 0
        self.lock = Lock()
    
    def increment(self, n: int):
        for _ in range(n):
            # self.lock.acquire()
            # self.cnt += 1
            # self.lock.release()
            with self.lock:
                self.cnt += 1


if __name__ == "__main__":

    counter = Counter()

    threads = [0] * N_THREADS

    for i in range(N_THREADS):
        threads[i] = threading.Thread(target=counter.increment, args=(int(TARGET_SUM/N_THREADS),))
    logger.info("Threads created")

    for i in range(N_THREADS):
        threads[i].start()
    logger.info("Threads started")

    for i in range(N_THREADS):
        threads[i].join()

    logger.info(f"Final value: {counter.cnt}")
