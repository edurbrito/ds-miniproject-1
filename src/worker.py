from logging import CRITICAL, DEBUG, ERROR, INFO, debug
from threading import Thread
from time import sleep

from __env__ import DO_NOT_WANT, HELD, PORT


class Worker(Thread):

    def __init__(self, node) -> None:
        self.node = node
        super().__init__()

    def run(self):
        while True:
            sleep(3)

            with self.node.lock:
                debug(msg=f"{str(self.node)} : " + str(self.node.queue))

            _to = (self.node.id % self.node.n_processes) + PORT

            self.node.send_message(_to, "HELLO")

            self.node.set_state(HELD)

            self.node.increment_timestamp()
