import time
from threading import Thread, current_thread


def task():
    while True:
        print(f"{current_thread().getName()} is executing!")
        time.sleep(1)


thread = Thread(target=task, name="RegularThread", daemon=False)
thread.start()

time.sleep(3)

print(f"{current_thread().getName()} is exiting!")
