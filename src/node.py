from multiprocessing import Process

from rpyc.utils.server import ThreadedServer

from __env__ import DO_NOT_WANT, HELD, OK, PORT, RELEASE, TIMESTAMP, WANTED
from rpc import RPCService
from worker import Worker


class Node(Process):
    def __init__(self, port, n_processes) -> None:
        super().__init__()
        self.id = port % PORT + 1
        self.port = port
        self.ports = list(range(PORT, PORT + n_processes))
        self.ports.remove(self.port)

        self.state = DO_NOT_WANT
        self.timeout_cs = (10, 10)
        self.timeout_p = (5, 5)
        self.timestamp = 0

        self.queue = []
        self.replies = {}
        self.n_processes = n_processes

        self.rpc_service = RPCService(self)
        self.worker = Worker(self)

    def __str__(self) -> str:
        return f"P{self.id}, {self.state}"

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

    def send_message(self, _to, _message):
        return self.rpc_service.send_message(_to, _message)

    def adjust_timestamp(self, timestamp):
        self.timestamp = max(self.timestamp, timestamp) + 1

    def increment_timestamp(self):
        self.timestamp += 1

    def set_wanted_state(self):
        if self.state == DO_NOT_WANT:
            self.state = WANTED
            self.increment_timestamp()

    def request_access(self, requested):
        if not requested:
            for port in self.ports:
                if port not in self.replies:
                    self.replies[port] = self.send_message(
                        port, (TIMESTAMP, self.timestamp, self.port))

        if len(self.replies) == self.n_processes - 1 and all(self.replies.values()):
            self.state = HELD
            self.increment_timestamp()
            self.replies = {}

    def handle_message(self, _message):
        type = _message[0]
        if type == RELEASE:
            _from = _message[1]
            self.replies[_from] = OK
        elif type == TIMESTAMP:
            timestamp, _from = _message[1], _message[2]
            if self.state == DO_NOT_WANT:
                self.adjust_timestamp(timestamp)
                return OK
            elif self.state == WANTED:
                if self.timestamp > timestamp or (self.timestamp == timestamp and self.port > _from):
                    return OK
                else:
                    self.queue.append(_message)
            elif self.state == HELD:
                self.queue.append(_message)
        return None

    def release(self):
        self.state = DO_NOT_WANT
        self.increment_timestamp()
        while len(self.queue) != 0:
            _, timestamp, port = self.queue.pop(0)
            self.adjust_timestamp(timestamp)
            self.rpc_service.send_message(port, (RELEASE, self.port))

    def run(self):
        self.worker.start()
        ThreadedServer(self.rpc_service, port=self.port).start()
