import random
from time import sleep


class CriticalSection():
    def __init__(self) -> None:
        self.process = None
        self.timeout = 10

    def set_timeout(self, t):
        if t > 10:
            self.timeout = random.randint(10, t)

    def assign_process(self, process):
        self.process = process
        sleep(self.timeout)
        self.process.release()
        self.process = None
