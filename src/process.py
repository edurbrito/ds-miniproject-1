import threading
import random
from time import sleep
from __env__ import *


class Process(threading.Thread):
    def __init__(self, id, event_observer):
        threading.Thread.__init__(self)
        self.id = id
        self.state = DO_NOT_WANT
        self.timeout = 5
        self.timestamp = 1
        self.event_observer = event_observer
        self.queue = []
        self.replies = {}

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
        if t > 5:
            self.timeout = random.randint(5, t)

    def set_wanted_state(self):
        if self.state == DO_NOT_WANT:
            self.state = WANTED
            self.event_observer.notify("onSetWantedState", self.id)

    def release(self):
        self.state = DO_NOT_WANT
        self.event_observer.notify("onRelease", (self.queue, self.id))

    def run(self):
        while True:
            sleep(self.timeout)
            self.set_wanted_state()
    
    def handle_message(self, message):
        timestamp, _ = message
        if self.state == DO_NOT_WANT:
            return "OK"
        elif self.state == HELD:
            self.queue.append(message)
            return None
        elif self.state == WANTED:
            if self.timestamp > timestamp:
                return "OK"
            else:
                self.queue.append(message)
                return None  
