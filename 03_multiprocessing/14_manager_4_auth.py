import multiprocessing
import os
import time
from multiprocessing import Process, Semaphore
from multiprocessing.managers import BaseManager, Server
from threading import Thread

from utils import logger


def host(port: int, semaphore: Semaphore, alive: int = 3):
    time.sleep(2)

    shared_string = "kek"

    manager = BaseManager(address=("127.0.0.1", port), authkey=b"228322")
    manager.register("get_shared_string", callable=lambda: shared_string)
    manager.start()
    logger.info("Host intialized!")
    semaphore.release()
    time.sleep(1)
    logger.info("Shutting down...")
    manager.shutdown()
    logger.info("Shot down!")


def proxy(port: int):
    manager = BaseManager(address=("127.0.0.1", port), authkey=b"228322")
    manager.register("get_shared_string")
    logger.info("Proxy waiting to connect...")
    manager.connect()
    logger.info("Proxy connected!")

    shared_string = manager.get_shared_string()

    logger.info(f"repr: {repr(shared_string)}")
    logger.info(f"shared object: {shared_string}")
    logger.info(shared_string.capitalize())


if __name__ == "__main__":

    multiprocessing.set_start_method("fork")

    logger.info(f"{os.cpu_count()} cores found!")

    port = 1337
    semaphore = Semaphore(0)

    host_process = Process(target=host, args=(port, semaphore), name="HostProcess")
    proxy_process_1 = Process(target=proxy, args=(port,), name="ProxyProcess-1")
    proxy_process_2 = Process(target=proxy, args=(port,), name="ProxyProcess-2")

    host_process.start()
    semaphore.acquire()

    proxy_process_1.start()
    proxy_process_2.start()

    host_process.join()
    proxy_process_1.join()
    proxy_process_2.join()

    logger.info("Exiting!")
