import multiprocessing
import os
from multiprocessing import Process, current_process

f = None


def task():
    f.write(f"{current_process().name} with pid {os.getpid()} and ppid {os.getppid()} writing to file\n")
    f.flush()
    # we can close here but in main process it won't close
    # because they don't share state
    f.close()


if __name__ == "__main__":
    filename = "./03_multiprocessing/02_fork_1_copying.txt"
    f = open(filename, "w")
    # task()

    multiprocessing.set_start_method("fork")
    process = Process(target=task)
    process.start()
    process.join()

    print(f.closed)
    f.close()

    with open(filename, 'r') as f:
        print(f.read())

    os.remove(filename)
