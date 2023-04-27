from utils import logger


def task():
    i = 0
    while True:
        i += 1
        yield i
        k = yield
        logger.info(f"Task received {k}")


def task_all_in_one():
    i = 0
    while True:
        i += 1
        k = yield i
        logger.info(f"Task received {k}")


if __name__ == "__main__":

    # gen = task()
    # logger.info(next(gen))
    # for i in range(10, 20):
    #     next(gen)
    #     logger.info(gen.send(i))

    gen_new = task_all_in_one()
    logger.info(next(gen_new))

    for i in range(10, 20):

        # next(gen_new)
        logger.info(gen_new.send(i))
