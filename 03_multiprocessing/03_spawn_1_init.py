import os
import time
from multiprocessing import Process, current_process, set_start_method
from threading import Lock, Thread, current_thread

import sample_import


def task():
    print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} is doing task!")


if __name__ == "__main__":

    set_start_method("spawn")
    # set_start_method("fork")

    task()
    process = Process(target=task)
    process.start()
    process.join()
