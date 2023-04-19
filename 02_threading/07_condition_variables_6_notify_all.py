import math
import time
from threading import Condition, Lock, Thread, current_thread

condition_lock = Condition(Lock())
condition_var = False


def task():
    condition_lock.acquire()

    while not condition_var:
        condition_lock.wait()
        print(f"{current_thread().getName()} woken up")

    condition_lock.release()
    print(f"{current_thread().getName()} exiting")


task_thread_1 = Thread(target=task)
task_thread_2 = Thread(target=task)
task_thread_3 = Thread(target=task)

task_thread_1.start()
task_thread_2.start()
task_thread_3.start()


condition_lock.acquire()
condition_var = True
condition_lock.notify(2)
condition_lock.release()
# time.sleep(3)

task_thread_1.join()
task_thread_2.join()
task_thread_3.join()
