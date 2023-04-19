import math
import time
from threading import Lock, Thread, current_thread

prime_found = False
prime_number = None


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes():
    global prime_found, prime_number
    n = 2
    while True:
        if is_prime(n):
            prime_found = True
            prime_number = n
            time.sleep(0.1)
        n += 1


def print_primes():
    global prime_found, prime_number
    while True:
        if prime_found:
            print(f"{current_thread().getName()} printing prime: {prime_number}")
            prime_found = False
        time.sleep(0.05)


find_primes_thread = Thread(target=find_primes, name="FindPrimesThread")
print_primes_thread = Thread(target=print_primes, name="FindPrimesThread")

find_primes_thread.start()
print_primes_thread.start()

find_primes_thread.join()
print_primes_thread.join()
