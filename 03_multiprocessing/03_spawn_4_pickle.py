import os
import time
from multiprocessing import Process, current_process, set_start_method
from threading import Lock, Thread, current_thread


def task(lock):
    with lock:
        print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} is doing task!")


if __name__ == "__main__":

    lock = Lock()

    # set_start_method("fork")
    set_start_method("spawn")

    process = Process(target=task, args=(lock,))
    process.start()
    process.join()
