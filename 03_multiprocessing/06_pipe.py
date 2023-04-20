import multiprocessing
from multiprocessing import Pipe, Process

from utils import logger


def task(conn):
    logger.info(f"Starting task!")
    for i in range(10):
        conn.send(i)
        logger.info("Sending value to pipe!")
    logger.info(f"Finished task!")


if __name__ == "__main__":

    multiprocessing.set_start_method("forkserver")
    logger.info(f"This machine has {multiprocessing.cpu_count()} CPUs")

    parent_conn, child_conn = Pipe()

    producer = Process(target=task, args=(parent_conn,))
    producer.start()

    for _ in range(10):
        logger.info(child_conn.recv())

    parent_conn.close()
    producer.join()

    logger.info("Exiting!")
