import math
import time
from threading import Event, Thread, current_thread

prime_number = None
keep_running = True
found_event = Event()
print_event = Event()


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
        found_event.set()
        print_event.wait()
        print_event.clear()
        n += 1
    found_event.set()
    # semaphore_print.release()


def print_primes():
    global prime_number
    while keep_running:
        found_event.wait()
        found_event.clear()
        print(f"{current_thread().getName()} printing prime: {prime_number}")
        prime_number = None
        print_event.set()


find_primes_thread = Thread(target=find_primes, name="FindPrimesThread")
print_primes_thread = Thread(target=print_primes, name="PrintPrimesThread")

find_primes_thread.start()
print_primes_thread.start()

time.sleep(0.001)
keep_running = False

find_primes_thread.join()
print_primes_thread.join()
