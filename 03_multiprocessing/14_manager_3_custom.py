import multiprocessing
import os
import time
from multiprocessing import Process, Semaphore
from multiprocessing.managers import BaseManager, Server
from threading import Thread

from utils import logger


class Utility:
    def capitalize(self, s: str) -> str:
        return s.capitalize()


class MyManager(BaseManager):
    pass


MyManager.register("Utility", Utility)


def host(port: int, semaphore: Semaphore, alive: int = 3):
    time.sleep(1)

    manager = MyManager(address=("127.0.0.1", port))
    manager.start()

    logger.info("Host intialized!")
    semaphore.release()
    time.sleep(1)

    logger.info("Shutting down...")
    manager.shutdown()
    logger.info("Shot down!")


def proxy(port: int, text: str):
    manager = MyManager(address=("127.0.0.1", port))
    manager.register("Utility")
    logger.info("Proxy waiting to connect...")
    manager.connect()
    logger.info("Proxy connected!")

    logger.info(manager.Utility().capitalize(text))


if __name__ == "__main__":

    multiprocessing.set_start_method("fork")

    logger.info(f"{os.cpu_count()} cores found!")

    port = 1337
    semaphore = Semaphore(0)

    host_process = Process(target=host, args=(port, semaphore), name="HostProcess")
    proxy_process_1 = Process(target=proxy, args=(port, "kek"), name="ProxyProcess-1")
    proxy_process_2 = Process(target=proxy, args=(port, "lol"), name="ProxyProcess-2")

    host_process.start()
    semaphore.acquire()

    proxy_process_1.start()
    proxy_process_2.start()

    host_process.join()
    proxy_process_1.join()
    proxy_process_2.join()

    logger.info("Exiting!")
