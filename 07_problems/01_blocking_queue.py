import time
from collections import deque
from ctypes import c_bool
from threading import Condition, Thread

from utils import logger


class BlockingQueue:
    def __init__(self):
        self.lock = Condition()
        self.queue = deque([])

    def put(self, val):
        with self.lock:
            self.queue.append(val)
            self.lock.notify_all()

    def get(self):
        global keep_running
        with self.lock:
            while not self.queue and keep_running:
                self.lock.wait()
            if keep_running:
                return self.queue.popleft()


def producer(q: BlockingQueue):
    global keep_running
    x = 0
    logger.info("Starting!")
    while keep_running:
        q.put(x)
        time.sleep(0.1)
        x += 1
    logger.info("Exiting!")


def consumer(q: BlockingQueue):
    global keep_running
    logger.info("Starting!")
    while keep_running:
        v = q.get()
        if keep_running:
            logger.info(v)
    logger.info("Exiting!")


if __name__ == "__main__":

    keep_running, queue = True, BlockingQueue()

    producer_thread = Thread(target=producer, args=(queue,), name="ProducerThread")
    consumer_thread_1 = Thread(target=consumer, args=(queue,), name="ConsumerThread-1")
    consumer_thread_2 = Thread(target=consumer, args=(queue,), name="ConsumerThread-2")

    producer_thread.start()
    consumer_thread_1.start()
    consumer_thread_2.start()

    time.sleep(3)

    logger.info("Shutting down...")
    keep_running = False
    with queue.lock:
        queue.lock.notify_all()

    producer_thread.join()
    consumer_thread_1.join()
    consumer_thread_2.join()
