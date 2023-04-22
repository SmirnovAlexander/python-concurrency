import math
import time
from ctypes import c_bool, c_int
from multiprocessing import Condition, Process, Value

from utils import logger


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def find_primes(keep_running: Value, prime_number: Value, condition_lock: Condition):
    n = 2
    while keep_running.value:
        if is_prime(n):
            with condition_lock:
                prime_number.value = n
                condition_lock.notify()

            with condition_lock:
                while prime_number.value and keep_running.value:
                    condition_lock.wait()
        n += 1


def print_primes(keep_running: Value, prime_number: Value, condition_lock: Condition):
    while keep_running.value:
        with condition_lock:
            while not prime_number.value and keep_running.value:
                condition_lock.wait()
            if keep_running.value:
                logger.info(f"{prime_number.value}")
                prime_number.value = 0
                condition_lock.notify_all()


if __name__ == "__main__":

    keep_running, prime_number, condition_lock = Value(c_bool, True), Value(c_int, 0), Condition()

    find_primes_process = Process(
        target=find_primes, args=(keep_running, prime_number, condition_lock), name="FindPrimesProcess"
    )
    print_primes_process_1 = Process(
        target=print_primes, args=(keep_running, prime_number, condition_lock), name="PrintPrimesProcess-1"
    )
    print_primes_process_2 = Process(
        target=print_primes, args=(keep_running, prime_number, condition_lock), name="PrintPrimesprocess-2"
    )

    find_primes_process.start()
    print_primes_process_1.start()
    print_primes_process_2.start()

    time.sleep(0.005)
    keep_running.value = False

    with condition_lock:
        condition_lock.notify_all()

    find_primes_process.join()
    print_primes_process_1.join()
    print_primes_process_2.join()
