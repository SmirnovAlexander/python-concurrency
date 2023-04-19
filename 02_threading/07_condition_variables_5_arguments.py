import math
import time
from threading import Condition, Lock, Thread, current_thread

condition_lock = Condition(Lock())
condition_var = False


def task():
    condition_lock.acquire()

    if not condition_var:
        condition_lock.wait(1)

    if not condition_var:
        print(f"{current_thread().getName()} timeouted waiting")

    condition_lock.release()


task_thread = Thread(target=task)

task_thread.start()
time.sleep(3)
task_thread.join()
