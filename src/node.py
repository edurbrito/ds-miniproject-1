from multiprocessing import Process
import random
from threading import Lock
from time import sleep

from rpyc.utils.server import ThreadedServer
from __env__ import DO_NOT_WANT, HELD, WANTED, PORT, OK

from rpc import RPCService
from worker import Worker


class Node(Process):
    def __init__(self, port, n_processes) -> None:
        super().__init__()
        self.id = port % PORT + 1
        self.port = port

        self.state = DO_NOT_WANT
        self.timeout_cs = (10, 15)
        self.cs_holding_time = 10
        self.timeout_p = (5, 9)
        self.timestamp = 0

        self.queue = []
        self.replies = {}
        self.n_processes = n_processes
        self.lock = Lock()

        self.rpc_service = RPCService(self)
        self.worker = Worker(self)

    def __str__(self) -> str:
        return f"P{self.id}, {self.state} - {self.timeout_cs} - {self.timeout_p} - {self.timestamp}"

    def __eq__(self, __o: 'Process') -> bool:
        return self.id == __o.id

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, __o: 'Process') -> bool:
        return self.timestamp < __o.timestamp

    def set_timeout_cs(self, t):
        if int(t) >= 10:
            self.timeout_cs = (10, int(t))
            return True
        return False

    def set_timeout_p(self, t):
        if int(t) >= 5:
            self.timeout_p = (5, int(t))
            return True
        return False

    def adjust_timestamp(self, timestamp):
        self.timestamp = max(self.timestamp, timestamp) + 1

    def increment_timestamp(self):
        self.timestamp += 1

    def set_wanted_state(self):
        if self.state == DO_NOT_WANT:
            self.state = WANTED
            self.increment_timestamp()
            self.request_access()

    def send_message(self, _to, _message):
        self.rpc_service.send_message(_to, _message)

    def respond(self, _to, _response):
        self.increment_timestamp()
        self.rpc_service.respond(_to, _response)

    def get_ports(self):
        ports = list(range(PORT, PORT + self.n_processes))
        ports.remove(self.port)
        return ports

    def request_access(self):
        ports = self.get_ports()

        self.increment_timestamp()
        for port in ports:
            self.send_message(port, (self.timestamp, self.port))

    def handle_message(self, _message):
        timestamp, _from = _message
        self.adjust_timestamp(timestamp)
        if self.state == DO_NOT_WANT:
            self.increment_timestamp()
            self.respond(_to=_from, _response=OK)
        elif self.state == HELD:
            self.queue.append(_message)
        elif self.state == WANTED:
            print(self.port, _from)
            if self.timestamp > timestamp or (self.timestamp == timestamp and self.port > _from):
                self.increment_timestamp()
                self.respond(_to=_from, _response=OK)
            else:
                self.queue.append(_message)

    def handle_response(self, _from, _response):
        self.replies[_from] = _response
        self.increment_timestamp()

        self.check_replies()

    def check_replies(self):
        if len(self.replies) == self.n_processes - 1 and all(self.replies.values()):
            self.state = HELD
            self.increment_timestamp()
            self.replies = {}

    def release(self):
        self.state = DO_NOT_WANT
        self.increment_timestamp()

        self.increment_timestamp()
        while len(self.queue) != 0:
            _, port = self.queue.pop(0)

            self.rpc_service.respond(port, OK)

    def run(self):
        self.worker.start()
        ThreadedServer(self.rpc_service, port=self.port).start()
