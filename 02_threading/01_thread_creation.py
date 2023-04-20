import threading
from threading import current_thread


def thread_tasks(a, b, c, key1, key2):
    print(f"{current_thread().name} received args: {a}, {b}, {c}, {key1}, {key2}")


thread = threading.Thread(
    group=None,
    target=thread_tasks,
    name="DemoThread",
    args=(1, 2, 3),
    kwargs={"key1": 777, "key2": 111},
    daemon=None,
)

print(f"Current thread: {current_thread().getName()}")
thread.start()
thread.join()
