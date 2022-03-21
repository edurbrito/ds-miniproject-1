import threading
from time import sleep
from __env__ import *


class Process(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        self.state = DO_NOT_WANT
        self.timeout = 5, 5  # min, max
        self.timestamp = 1

    def __str__(self) -> str:
        return f"P{self.id}, {self.state}"

    def __eq__(self, __o: 'Process') -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, __o: 'Process') -> bool:
        return self.timestamp < __o.timestamp

    def set_timeout(self, t):
        if t >= 5:
            self.timeout = 5, t

    def run(self):
        while True:
            sleep(3)
