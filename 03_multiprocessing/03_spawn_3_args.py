import os
import time
from multiprocessing import Process, current_process, set_start_method
from threading import Lock, Thread, current_thread

global_arg = "kek"


def task(arg1, arg2):
    print(
        f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} is doing task with args {arg1}, {arg2}!"
    )


if __name__ == "__main__":

    # set_start_method("fork")
    set_start_method("spawn")
    local_arg = "lol"

    process = Process(target=task, args=(global_arg, local_arg))
    process.start()
    process.join()
