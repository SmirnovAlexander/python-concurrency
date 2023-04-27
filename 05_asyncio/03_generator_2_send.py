from utils import logger


def task():
    while True:
        item = yield
        logger.info(f"Task received {item}")


if __name__ == "__main__":

    gen = task()
    gen.send(None)

    logger.info(next(gen))
    logger.info(next(gen))
    gen.send(37)
