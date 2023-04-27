import inspect

from utils import logger


def natural_nums():
    n = 1
    try:
        while True:
            yield n
            n += 1
    except GeneratorExit:
        logger.info("GeneratorExit exception raised")


if __name__ == "__main__":

    gen = natural_nums()
    logger.info(inspect.getgeneratorstate(gen))
    logger.info(next(gen))
    logger.info(inspect.getgeneratorstate(gen))
    gen.close()
    logger.info(inspect.getgeneratorstate(gen))
