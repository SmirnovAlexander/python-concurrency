from utils import logger

if __name__ == "__main__":
    lst = [1, 2, 3]

    # get iterator of list using __iter__()
    it = lst.__iter__()
    logger.info("iterator of list: " + str(it))

    # get member element of list using __getitem__()
    logger.info("member of list: " + str(lst.__getitem__(2)))

    # iterator returns itself when passed to the iter function
    logger.info("it is iter(it) = " + str(it is iter(it)))

    # get another iterator for list using the built in iter() method
    it_another = iter(lst)
    logger.info("it_another = " + str(it_another))

    logger.info("iteration using iterator in a for loop")
    # iterate using the iterator
    for element in it_another:
        logger.info(element)

    logger.info("iteration using iterable in a for loop")
    # iterate using the iterable
    for element in lst:
        logger.info(element)
