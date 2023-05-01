import time
from concurrent.futures import ThreadPoolExecutor, wait
from threading import Condition, Lock, Semaphore, Thread

from utils import logger


class Barber:
    def __init__(self, n):
        self.n = n
        self.chairs_cnt = n
        self.lock = Condition()
        self.wait_for_customers_to_enter = Semaphore(0)
        self.wait_for_barber_to_be_ready = Semaphore(0)
        self.wait_for_haircut_finished = Semaphore(0)
        self.wait_for_customer_to_leave = Semaphore(0)

    def start(self):
        logger.info("Starting work!")
        while True:
            self.wait_for_customers_to_enter.acquire()
            self.wait_for_barber_to_be_ready.release()
            time.sleep(1)
            self.wait_for_haircut_finished.release()
            self.wait_for_customer_to_leave.acquire()

    def request_haircut(self) -> bool:
        logger.info("Requestin haircut!")
        with self.lock:
            if self.chairs_cnt == 0:
                logger.info("All chairs are busy, exiting!")
                return False
            self.chairs_cnt -= 1
            logger.info("Had a seat!")

        logger.info("Notifying barber that customer came")
        self.wait_for_customers_to_enter.release()

        logger.info("Waiting for barber to be ready")
        self.wait_for_barber_to_be_ready.acquire()

        with self.lock:
            self.chairs_cnt += 1

        logger.info("Waiting for haircut to be finished")
        self.wait_for_haircut_finished.acquire()

        logger.info("Leaving barbershop")
        self.wait_for_customer_to_leave.release()

        return True


if __name__ == "__main__":

    n_chairs, n_visitors = 3, 10

    barber = Barber(n_chairs)
    Thread(target=barber.start, name="BarberThread", daemon=True).start()
    time.sleep(0.5)

    pool = ThreadPoolExecutor(thread_name_prefix="Customer")
    futures = []
    for _ in range(n_visitors):
        futures.append(pool.submit(barber.request_haircut))
        # time.sleep(0.5)

    cnt = 0
    for f in wait(futures)[0]:
        cnt += f.result()

    logger.info(cnt)

    logger.info("Exiting!")
