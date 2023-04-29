import random
import time
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from threading import Barrier, Lock, Semaphore

from utils import logger


class Party(Enum):
    REPUBLICAN = 0
    DEMOCRAT = 1

    def get_other_party(self):
        return next(v for v in Party if v != self)


class UberSeatingServer:
    def __init__(self):

        self.ride_cnt = 0
        self.requesters_cnt = {v.name: 0 for v in Party}
        self.current_car = {v.name: 0 for v in Party}

        self.lock = Lock()
        self.barrier = Barrier(4)
        self.semaphores = {v.name: Semaphore(0) for v in Party}

    def drive(self):
        self.ride_cnt += 1
        logger.info(f"Ride #{self.ride_cnt} departed with {self.current_car} on board!")
        self.current_car = {v.name: 0 for v in Party}
        # logger.info(self.requesters_cnt)

    def seated(self, party: Party):
        # probably not thread safe when
        # not lead_passenger get released and seated
        self.current_car[party.name] += 1
        logger.info(f"{party.name} party member seated!")

    def request_ride(self, party: Party):

        logger.info(f"{party.name} party member requested a ride!")

        lead_passenger = False

        self.lock.acquire()

        self.requesters_cnt[party.name] += 1
        if self.requesters_cnt[party.name] == 4:
            lead_passenger = True
            self.semaphores[party.name].release()
            self.semaphores[party.name].release()
            self.semaphores[party.name].release()
            self.requesters_cnt[party.name] -= 4
        elif self.requesters_cnt[party.name] >= 2 and self.requesters_cnt[party.get_other_party().name] >= 2:
            lead_passenger = True
            self.semaphores[party.name].release()
            self.semaphores[party.get_other_party().name].release()
            self.semaphores[party.get_other_party().name].release()
            self.requesters_cnt[party.name] -= 2
            self.requesters_cnt[party.get_other_party().name] -= 2
        else:
            self.lock.release()
            self.semaphores[party.name].acquire()

        self.seated(party)
        self.barrier.wait()

        if lead_passenger:
            self.drive()
            self.lock.release()


if __name__ == "__main__":

    n_requesters = 16

    server = UberSeatingServer()
    pool = ThreadPoolExecutor(thread_name_prefix="Passenger")

    futures = []
    for _ in range(n_requesters):
        futures.append(pool.submit(server.request_ride, random.choice(list(Party))))
        # time.sleep(0.1)
