import heapq
import random
import time
from threading import Condition, Thread
from typing import Callable, Tuple

from utils import logger


class DeferredCallbackExecutor:
    def __init__(self):
        self.lock = Condition()
        self.heap = []
        self.start_thread = Thread(target=self.start, name="DeferredCallbackExecutorThread", daemon=True)
        self.start_thread.start()

    def schedule(self, fn: Callable, args: Tuple, delay: int):
        logger.info(f"Received task for execution with delay {delay} and args {args}")
        with self.lock:
            heapq.heappush(self.heap, (int(time.time()) + delay, (fn, args)))
            self.lock.notify()

    def start(self):
        while True:
            with self.lock:
                while not self.heap:
                    self.lock.wait()

                while True:
                    execute_time, _ = self.heap[0]
                    wait_time = execute_time - int(time.time())
                    if wait_time <= 0:
                        break
                    self.lock.wait(timeout=wait_time)

                _, (fn, args) = heapq.heappop(self.heap)
                fn(*args)


def task(x: int):
    logger.info(f"Finished task with args {x}")


if __name__ == "__main__":

    executor = DeferredCallbackExecutor()

    futures = []
    for _ in range(5):
        x, delay = random.randrange(10, 20), random.randrange(5)
        executor.schedule(task, (x,), delay)

    time.sleep(7)
