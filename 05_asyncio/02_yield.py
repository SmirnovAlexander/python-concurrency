import math

from utils import logger


def task():
    return "kek"


def task_async():
    yield "kek_async"
    yield "kek_async_2"
    return "kek_async_3"


def is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_primes():
    n = 2
    while True:
        while not is_prime(n):
            n += 1
        yield n
        n += 1


if __name__ == "__main__":

    logger.info(task())
    gen = task_async()
    # for item in gen:
    #     logger.info(item)
    logger.info(next(gen))
    logger.info(next(gen))

    try:
        next(gen)
    except StopIteration as e:
        logger.info(e.value)

    primes_generator = get_primes()

    primes = [next(primes_generator) for _ in range(10)]
    logger.info(primes)

    logger.info(next(primes_generator))
    logger.info(next(primes_generator))
    logger.info(next(primes_generator))
    logger.info(next(primes_generator))
