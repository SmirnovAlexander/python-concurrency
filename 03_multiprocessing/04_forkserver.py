import multiprocessing
import os
from multiprocessing import Process

import sample_import
from utils import logger

global_var = "kek"


def task():
    logger.info(f"Starting task!")
    logger.info(global_var)


if __name__ == "__main__":

    # set_start_method("fork")
    # set_start_method("spawn")
    multiprocessing.set_start_method("forkserver")
    # on the start of the program it spawns
    # a clean new process at the beginning
    # and forks from it

    global_var = "lol"

    process = Process(target=task)
    process.start()
    process.join()
