import random
import time
from threading import Barrier, Thread, current_thread


def task():
    time.sleep(random.randint(1, 4))
    print(f"{current_thread().getName()} is blocked on barrier ({barrier.n_waiting})")
    barrier.wait()


def on_exit():
    print(f"{current_thread().getName()} telling that barrier ({barrier.n_waiting}) is gone")


n_threads = 5
barrier = Barrier(n_threads, action=on_exit)

threads = [Thread(target=task) for _ in range(n_threads)]
for i in range(n_threads):
    threads[i].start()

# print(f"{current_thread().getName()} is aborting barrer")
# barrier.abort()

print(f"{current_thread().getName()} exiting")
