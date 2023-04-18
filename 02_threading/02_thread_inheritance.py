from threading import Thread, current_thread


class MyTask(Thread):
    def __init__(self, a, b):
        self.a, self.b = a, b
        Thread.__init__(self, name="MyTaskThread")

    def run(self):
        print(f"{current_thread().getName()} is executing with args {self.a}, {self.b}")


task = MyTask(2, 3)

task.start()
task.join()

print(f"{current_thread().getName()} is exiting")
