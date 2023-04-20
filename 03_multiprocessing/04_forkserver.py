import os
import time
from multiprocessing import Process, current_process, set_start_method
from threading import Lock, Thread, current_thread

import sample_import

global_var = "kek"


def task():
    print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} is doing task!")
    print(global_var)


if __name__ == "__main__":

    # set_start_method("fork")
    # set_start_method("spawn")
    set_start_method("forkserver")
    # on the start of the program it spawns
    # a clean new process at the beginning
    # and forks from it

    global_var = "lol"

    process = Process(target=task)
    process.start()
    process.join()
