import math
import time
from threading import Condition, Lock, Thread, current_thread

prime_found = False
prime_number = None
keep_running = True
condition_lock = Condition()


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes():
    global prime_found, prime_number, condition_lock
    n = 2
    while keep_running:
        if is_prime(n):
            condition_lock.acquire()
            prime_found = True
            prime_number = n
            condition_lock.notify()
            condition_lock.release()

            condition_lock.acquire()
            while prime_found and keep_running:
                condition_lock.wait()
            condition_lock.release()
        n += 1


def print_primes():
    global prime_found, prime_number, condition_lock
    while keep_running:
        condition_lock.acquire()
        while not prime_found and keep_running:
            condition_lock.wait()
        if keep_running:
            print(f"{current_thread().getName()} printing prime: {prime_number}")
            prime_found = False
            condition_lock.notify_all()
        condition_lock.release()


find_primes_thread = Thread(target=find_primes, name="FindPrimesThread")
print_primes_thread_1 = Thread(target=print_primes, name="PrintPrimesThread1")
print_primes_thread_2 = Thread(target=print_primes, name="PrintPrimesThread2")

find_primes_thread.start()
print_primes_thread_1.start()
print_primes_thread_2.start()

time.sleep(0.001)
keep_running = False
condition_lock.acquire()
condition_lock.notify_all()
condition_lock.release()

find_primes_thread.join()
print_primes_thread_1.join()
print_primes_thread_2.join()
