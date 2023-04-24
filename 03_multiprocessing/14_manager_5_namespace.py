import multiprocessing
from multiprocessing import Process
from multiprocessing.managers import Namespace, SyncManager

from utils import logger


def task1(ns: Namespace):
    logger.info(ns.item)
    ns.item = "task1"
    logger.info(ns.item)


def task2(ns: Namespace):
    logger.info(ns.item)
    ns.item = "task2"
    logger.info(ns.item)


if __name__ == "__main__":

    multiprocessing.set_start_method("spawn")

    manager = SyncManager(address=("", 1337))
    manager.start()
    ns = manager.Namespace()
    ns.item = "main"

    task1_process = Process(target=task1, args=(ns,))
    task1_process.start()
    task1_process.join()

    task2_process = Process(target=task2, args=(ns,))
    task2_process.start()
    task2_process.join()
