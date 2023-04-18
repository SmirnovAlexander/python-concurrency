import time
from threading import RLock, Thread, current_thread

rlock = RLock()


def task():
    rlock.acquire()
    print(f"{current_thread().getName()} is working!")
    rlock.release()


rlock.acquire()
rlock.acquire()

rlock.release()
rlock.release()

thread = Thread(target=task)
thread.start()
thread.join()
