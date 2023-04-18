import time
from threading import Lock, Thread, current_thread


def task1(lock1, lock2):
    print(f"{current_thread().getName()} is atempting to acquire the lock1!")
    lock1.acquire()
    print(f"{current_thread().getName()} acquired the lock1!")
    time.sleep(1)
    print(f"{current_thread().getName()} is about to release the lock2!")
    lock2.release()
    print(f"{current_thread().getName()} released the lock2!")


# def task2(lock1, lock2):
#     print(f"{current_thread().getName()} is atempting to acquire the lock2!")
#     lock2.acquire()
#     print(f"{current_thread().getName()} acquired the lock2!")
#     time.sleep(1)
#     print(f"{current_thread().getName()} is about to release the lock1!")
#     lock1.release()
#     print(f"{current_thread().getName()} released the lock1!")


if __name__ == "__main__":

    lock1, lock2 = Lock(), Lock()

    thread1 = Thread(target=task1, args=(lock1, lock2))
    thread2 = Thread(target=task1, args=(lock1, lock2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
