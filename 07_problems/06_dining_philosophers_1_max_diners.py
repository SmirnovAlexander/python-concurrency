import random
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Semaphore

from utils import logger


class DiningPhilosophersServer:
    def __init__(self, n):

        self.n = n
        self.forks = [Semaphore(1) for _ in range(n)]
        # self.forks = [Lock() for _ in range(n)]

        self.max_diners = Semaphore(n - 1)
        # self.max_diners = Semaphore(n)

    def contemplate(self, idx):
        # contemplate_time = random.randrange(1, 6) / 10
        contemplate_time = 0
        logger.info(f"Philosopher {idx} started to contemplate for {contemplate_time}s...")
        time.sleep(contemplate_time)

    def eat(self, idx):
        self.max_diners.acquire()

        # eat_time = random.randrange(1, 6) / 10
        eat_time = 0

        left_fork, right_fork = self.forks[(idx + self.n - 1) % self.n], self.forks[idx]
        logger.info(f"Philosopher {idx} wants to acquire forks...")

        left_fork.acquire()
        # easier to get deadlock with this
        time.sleep(0.001)
        right_fork.acquire()

        logger.info(f"Philosopher {idx} starts eating for {eat_time}s...")
        time.sleep(eat_time)

        left_fork.release()
        right_fork.release()

        self.max_diners.release()


def start_philosopher(idx, server: DiningPhilosophersServer):
    while True:
        server.contemplate(idx)
        server.eat(idx)


if __name__ == "__main__":

    n_philosophers = 5

    server = DiningPhilosophersServer(n_philosophers)
    pool = ThreadPoolExecutor(thread_name_prefix="Philosopher")

    futures = []

    for i in range(n_philosophers):
        futures.append(pool.submit(start_philosopher, i, server))
