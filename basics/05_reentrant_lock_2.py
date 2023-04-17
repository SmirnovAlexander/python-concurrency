from threading import *


if __name__ == "__main__":
  ordinary_lock = RLock()
  ordinary_lock.acquire()
  ordinary_lock.acquire()
  
  print("{0} exiting".format(current_thread().getName()))

  ordinary_lock.release()
  ordinary_lock.release()
