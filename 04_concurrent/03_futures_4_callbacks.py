import time
from concurrent.futures import Future, ThreadPoolExecutor

from utils import logger


def task(x):
    logger.info(f"Executing task with arg {x}")
    time.sleep(3)
    return x * x


def done_callback(future: Future):
    res = future.result()
    logger.info(f"Hello from done callback with res: {res}")


def done_callback_2(future: Future):
    res = future.result()
    logger.info(f"Hello from done callback with res: {res * res}")


if __name__ == '__main__':

    executor = ThreadPoolExecutor()

    future = executor.submit(task, 10)
    future.add_done_callback(done_callback)
    future.add_done_callback(done_callback_2)

    logger.info("Exiting...")

    executor.shutdown(wait=False)

    logger.info("Executor shut down!")
