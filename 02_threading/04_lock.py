import time
from threading import Lock, Thread, current_thread

shared_state = [1, 2, 3]
lock = Lock()


def change_state():
    lock.acquire()
    print(f"{current_thread().getName()} aquired the lock!")

    time.sleep(3)
    shared_state[0] = 322

    print(f"{current_thread().getName()} is about to release the lock!")
    lock.release()
    print(f"{current_thread().getName()} released the lock!")


def print_state():
    print(f"{current_thread().getName()} is atempting to acquire the lock!")
    lock.acquire()
    print(f"{current_thread().getName()} aquired the lock!")

    print(shared_state)

    print(f"{current_thread().getName()} is about to release the lock!")
    lock.release()
    print(f"{current_thread().getName()} released the lock!")


if __name__ == "__main__":

    change_state_thread = Thread(target=change_state, name="ChangeStateThread")
    change_state_thread.start()

    print_state_thread = Thread(target=print_state, name="PrintStateThread")
    print_state_thread.start()

    change_state_thread.join()
    print_state_thread.join()
