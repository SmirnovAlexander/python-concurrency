import os
import time
from multiprocessing import Process, current_process
from threading import Lock, Thread, current_thread

lock = Lock()


def task():
    print(
        f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} attempting to acquire the lock!"
    )
    with lock:
        time.sleep(0.01)
        print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} acquired lock!")
        print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} is doing task!")
        print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} released lock!")


task()

process = Process(target=task)
# process = Thread(target=task)

print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} attempting to acquire the lock!")
lock.acquire()
print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} acquired lock!")

process.start()

lock.release()
print(f"{os.getppid()}-{os.getpid()}-{current_process().name}-{current_thread().name} released lock!")

process.join()
