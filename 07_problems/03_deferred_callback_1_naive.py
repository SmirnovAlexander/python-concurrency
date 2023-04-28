import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread
from typing import Callable, Tuple

from utils import logger


class DeferredCallbackExecutor:
    def __init__(self):
        self.pool = ThreadPoolExecutor()

    def execute(self, fn: Callable, args: Tuple, delay: int):
        time.sleep(delay)
        fn(*args)

    def schedule(self, fn: Callable, args: Tuple, delay: int):
        logger.info(f"Received task for execution with delay {delay} and args {args}")
        future = self.pool.submit(self.execute, fn, args, delay)
        return future


def task(x: int):
    logger.info(f"Finished task with args {x}")


if __name__ == "__main__":

    executor = DeferredCallbackExecutor()

    futures = []
    for _ in range(5):
        x, delay = random.randrange(10, 20), random.randrange(5)
        futures.append(executor.schedule(task, (x,), delay))

    for future in as_completed(futures):
        future.result()
