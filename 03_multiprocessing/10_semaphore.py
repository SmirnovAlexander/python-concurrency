import multiprocessing
import time
from ctypes import c_bool
from multiprocessing import Process, Semaphore, Value

from utils import logger


def ping(s1: Semaphore, s2: Semaphore, v: Value):
    while v.value:
        logger.info("ping")
        s2.release()
        s1.acquire()


def pong(s1: Semaphore, s2: Semaphore, v: Value):
    while v.value:
        s2.acquire()
        logger.info("pong")
        s1.release()


if __name__ == "__main__":

    s1, s2, v = Semaphore(0), Semaphore(0), Value(c_bool, True)

    ping_process = Process(target=ping, args=(s1, s2, v), name="PingProcess")
    pong_process = Process(target=pong, args=(s1, s2, v), name="PongProcess")

    ping_process.start()
    pong_process.start()

    time.sleep(0.005)
    v.value = False
    logger.info("Changed value!")

    ping_process.join()
    pong_process.join()
