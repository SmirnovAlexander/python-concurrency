import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Condition, Thread

from utils import logger


class TokenBucketFilter:
    def __init__(self, max_tokens: int, period: int = 1):
        self.max_tokens = max_tokens
        self.cur_tokens = max_tokens
        self.period = period
        self.lock = Condition()

        self.increment_thread = Thread(target=self.increment, name="ProducerThread", daemon=True)
        self.increment_thread.start()

    def increment(self):
        logger.info("Initializing increment thread...")
        while True:
            with self.lock:
                while self.cur_tokens == self.max_tokens:
                    self.lock.wait()
                self.cur_tokens += 1
                self.lock.notify_all()
            time.sleep(self.period)

    def get_token(self):
        with self.lock:
            while not self.cur_tokens:
                self.lock.wait()
            self.cur_tokens -= 1
            self.lock.notify_all()
        logger.info("Granting token!")
        return


if __name__ == "__main__":

    token_bucket_filter = TokenBucketFilter(max_tokens=5, period=1)
    pool = ThreadPoolExecutor()

    futures = []
    for i in range(20):
        futures.append(pool.submit(token_bucket_filter.get_token))

    for res in as_completed(futures):
        res.result()

    pool.shutdown()
