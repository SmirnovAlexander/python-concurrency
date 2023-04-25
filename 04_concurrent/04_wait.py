import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, wait

from utils import logger


def task(x: int) -> int:
    logger.info(f"Doing task with arg {x}")
    time.sleep(random.randrange(5))
    logger.info(f"Finished task with arg {x}")
    return x * x


if __name__ == "__main__":

    thread_executor = ThreadPoolExecutor()
    process_executor = ProcessPoolExecutor()

    futures = []

    futures.extend([thread_executor.submit(task, i) for i in range(5)])
    futures.extend([process_executor.submit(task, i) for i in range(5, 10)])

    # res = wait(futures, timeout=0.01, return_when="ALL_COMPLETED")
    res = wait(futures, return_when="FIRST_COMPLETED")

    logger.info(f"Completed futures count: {len(res.done)}")
    logger.info(f"Uncompleted futures count: {len(res.not_done)}")

    for v in res.done:
        logger.info(v.result())

    thread_executor.shutdown(wait=False)
    process_executor.shutdown(wait=False)

    logger.info("Exiting...")
