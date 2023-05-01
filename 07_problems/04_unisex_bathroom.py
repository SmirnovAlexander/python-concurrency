import random
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from threading import Condition, Semaphore

from utils import logger


class Sex(Enum):
    MALE = 0
    FEMALE = 1

    def get_other_sex(self):
        return next((v for v in list(Sex) if v != self))


class Bathroom:
    def __init__(self, n):
        self.n = n
        self.current_sex: Sex = None
        self.people_in = 0
        self.sem = Semaphore(n)
        self.lock = Condition()

    def use_bathroom(self, sex: Sex):
        logger.info(f"{sex.name} using bathroom ({self.people_in} people in)")
        time.sleep(1)

    def request_bathroom(self, sex: Sex):
        logger.info(f"{sex.name} requesting bathroom")
        with self.lock:
            while self.current_sex == sex.get_other_sex():
                self.lock.wait()
            self.sem.acquire()
            self.current_sex = sex
            self.people_in += 1

        self.use_bathroom(sex)
        self.sem.release()

        with self.lock:
            self.people_in -= 1
            if not self.people_in:
                self.current_sex = None
            self.lock.notify_all()


if __name__ == "__main__":

    capacity, n_people = 3, 10

    bathroom = Bathroom(3)

    pool = ThreadPoolExecutor(thread_name_prefix="Visitor")

    futures = []
    for _ in range(n_people):
        futures.append(pool.submit(bathroom.request_bathroom, random.choice(list(Sex))))

    logger.info("Exiting!")
