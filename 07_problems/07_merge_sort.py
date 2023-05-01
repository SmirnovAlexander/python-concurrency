import random
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from utils import logger

# pool = ProcessPoolExecutor()


pool = ThreadPoolExecutor(max_workers=2)


def merge_sort(start, end, lst):
    logger.info(f"Received {start} {end}")
    if start == end:
        return [lst[start]]
    else:
        l = merge_sort(start, (start + end) // 2, lst)
        r = merge_sort((start + end) // 2 + 1, end, lst)
        # l_f = pool.submit(merge_sort, start, (start + end) // 2, lst)
        # r_f = pool.submit(merge_sort, (start + end) // 2 + 1, end, lst)
        # l, r = l_f.result(), r_f.result()

        res, i, j, n, m = [], 0, 0, len(l), len(r)
        while i < n and j < m:
            if l[i] < r[j]:
                res.append(l[i])
                i += 1
            else:
                res.append(r[j])
                j += 1
        while i < n:
            res.append(l[i])
            i += 1
        while j < m:
            res.append(r[j])
            j += 1
        return res


if __name__ == "__main__":

    n = 10000000

    lst = [random.randrange(n) for _ in range(n)]
    logger.info(f"Starting sorting list of size {n}...")
    # logger.info(lst)

    lst_sorted = merge_sort(0, n - 1, lst)
    logger.info(f"Finished sorting!")
    # logger.info(lst_sorted)
    sanity_check = sorted(lst)

    logger.info(f"If list is sorted: {sanity_check == lst_sorted}")
