import threading
import random
import time

val = 0
lock = threading.Lock()

def updater():
    global val, lock
    while True:
        with lock:
            val = random.randint(1, 9)

def validator():
    global val
    while True:
        with lock:
            if val % 5 == 0:
                if val % 5 != 0:
                    print(val)

if __name__ == "__main__":
    updater_thread = threading.Thread(target=updater)
    validator_thread = threading.Thread(target=validator)

    updater_thread.start()
    validator_thread.start()
    
    time.sleep(5)
