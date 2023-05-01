import time
from threading import Condition, Semaphore, Thread

from utils import logger


class AsyncExecutor:
    def work(self, callback):
        time.sleep(5)
        callback()

    def execute_async(self, callback):
        Thread(target=self.work, args=(callback,)).start()


class SyncExecutor(AsyncExecutor):
    def __init__(self):
        self.sem = Semaphore(0)

    def work(self, callback):
        super().work(callback)
        self.sem.release()

    def execute_async(self, callback):
        super().execute_async(callback)
        self.sem.acquire()


class SyncExecutor2(AsyncExecutor):
    def __init__(self):
        self.lock = Condition()

    def work(self, callback):
        with self.lock:
            super().work(callback)
            self.lock.notify()

    def execute_async(self, callback):
        with self.lock:
            super().execute_async(callback)
            self.lock.wait()


def say_hi():
    logger.info("Hi")


if __name__ == "__main__":
    # executor = AsyncExecutor()
    # executor = SyncExecutor()
    executor = SyncExecutor2()
    executor.execute_async(say_hi)

    logger.info("main thread exiting")
