import math
import time
from threading import Condition, Lock, Semaphore, Thread, current_thread

prime_number = None
keep_running = True
semaphore_find = Semaphore(0)
semaphore_print = Semaphore(0)


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes():
    global prime_number
    n = 2
    while keep_running:
        while not is_prime(n):
            n += 1
        prime_number = n
        semaphore_print.release()
        print(f"{current_thread().getName()} released semaphore_print")
        semaphore_find.acquire()
        print(f"{current_thread().getName()} acquired semaphore_find")
        n += 1
    semaphore_print.release()


def print_primes():
    global prime_number
    while keep_running:
        semaphore_print.acquire()
        print(f"{current_thread().getName()} acquired semaphore_print ({semaphore_print._value})")
        print(f"{current_thread().getName()} printing prime: {prime_number}")
        prime_number = None
        semaphore_find.release()
        print(f"{current_thread().getName()} released semaphore_find")


find_primes_thread = Thread(target=find_primes, name="FindPrimesThread")
print_primes_thread = Thread(target=print_primes, name="PrintPrimesThread")

find_primes_thread.start()
print_primes_thread.start()

time.sleep(0.001)
keep_running = False

find_primes_thread.join()
print_primes_thread.join()
