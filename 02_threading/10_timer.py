import time
from threading import Timer, current_thread


def task(arg):
    print(f"{current_thread().getName()} is executing with arg {arg}")


timer = Timer(interval=1, function=task, args=(228,))
timer.start()

time.sleep(2)

print(f"{current_thread().getName()} exiting")
