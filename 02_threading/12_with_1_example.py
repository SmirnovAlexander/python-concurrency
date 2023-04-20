class Example(object):
    def __init__(self, val):
        self.val = val

    def display(self):
        # 1/0
        print(self.val)

    def __enter__(self):
        print("enter invoked")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"exit invoked with args: {exc_type}, {exc_val}, {exc_tb}")


with Example("kek") as example:
    example.display()
