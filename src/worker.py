import random
from threading import Thread
from time import sleep

from __env__ import DO_NOT_WANT, HELD, WANTED


class Worker(Thread):

    def __init__(self, node) -> None:
        self.node = node
        super().__init__()

    def get_timeout(self, interval):
        return random.randint(interval[0], interval[1])

    def run(self):
        requested = False
        while True:
            if self.node.state == DO_NOT_WANT:
                sleep(self.get_timeout(self.node.timeout_p))
                self.node.set_wanted_state()
                requested = False
            elif self.node.state == WANTED:
                self.node.request_access(requested)
                requested = True
            elif self.node.state == HELD:
                sleep(self.get_timeout(self.node.timeout_cs))
                self.node.release()
