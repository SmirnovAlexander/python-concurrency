import os
from multiprocessing import Process, current_process


def task(a, b, c, key1, key2):
    print(f"{current_process().name} is working with pid {os.getpid()} and ppid {os.getppid()}!")
    print(f"{current_process().name} received args: {a}, {b}, {c}, {key1}, {key2}")


n_processes = 3

processes = [None] * n_processes

for i in range(n_processes):
    processes[i] = Process(target=task, args=(i, i + 1, i + 2), kwargs={"key1": i, "key2": i + 1})

for i in range(n_processes):
    processes[i].start()

for i in range(n_processes):
    processes[i].join()


print(f"{current_process().name} has pid {os.getpid()} and ppid {os.getppid()}!")
