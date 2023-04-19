import math
import time
from threading import Condition, Lock, Thread, current_thread

prime_found = False
prime_number = None
condition_lock = Condition()


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes():
    global prime_found, prime_number, condition_lock
    n = 2
    while n < 100:
        if is_prime(n):
            condition_lock.acquire()
            prime_found = True
            prime_number = n
            condition_lock.notify()
            condition_lock.release()

            condition_lock.acquire()
            while prime_found:
                condition_lock.wait()
            condition_lock.release()
        n += 1


def print_primes():
    global prime_found, prime_number, condition_lock
    while True:
        condition_lock.acquire()
        while not prime_found:
            condition_lock.wait()
        condition_lock.release()

        condition_lock.acquire()
        print(f"{current_thread().getName()} printing prime: {prime_number}")
        prime_found = False
        condition_lock.notify()
        condition_lock.release()


find_primes_thread = Thread(target=find_primes, name="FindPrimesThread")
print_primes_thread = Thread(target=print_primes, name="FindPrimesThread")

find_primes_thread.start()
print_primes_thread.start()

find_primes_thread.join()
print_primes_thread.join()
