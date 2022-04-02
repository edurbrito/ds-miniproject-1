from logging import CRITICAL, DEBUG, ERROR, INFO, debug
from threading import Thread
from time import sleep
import random

from __env__ import DO_NOT_WANT, HELD, PORT, WANTED


class Worker(Thread):

    def __init__(self, node) -> None:
        self.node = node
        super().__init__()

    @staticmethod
    def get_timeout(interval):
        return random.randint(interval[0], interval[1])

    def run(self):
        while True:
            sleep(self.get_timeout(self.node.timeout_p))

            with self.node.lock:
                debug(msg=f"{str(self.node)} : " + str(self.node.queue))

            self.node.set_wanted_state()

            if self.node.state == HELD:
                sleep(self.get_timeout(self.node.timeout_cs))
                self.node.release()
