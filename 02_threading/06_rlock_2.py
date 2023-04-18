import time
from threading import RLock, Thread, current_thread

rlock = RLock()


def task():
    rlock.release()
    print(f"{current_thread().getName()} is working!")


rlock.acquire()
rlock.acquire()

rlock.release()

thread = Thread(target=task)
thread.start()
thread.join()
