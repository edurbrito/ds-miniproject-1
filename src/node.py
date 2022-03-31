from multiprocessing import Process
from threading import Lock

from rpyc.utils.server import ThreadedServer
from __env__ import DO_NOT_WANT, HELD, WANTED, PORT

from rpc import RPCService
from worker import Worker


class Node(Process):
    def __init__(self, port, n_processes) -> None:
        super().__init__()
        self.id = port % PORT + 1
        self.port = port

        self.state = DO_NOT_WANT
        self.timeout_cs = (10, 10)
        self.timeout_p = (5, 5)
        self.timestamp = 0

        self.queue = []
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

    def set_state(self, state):
        if state in [HELD, WANTED, DO_NOT_WANT]:
            self.state = state

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

    def set_timestamp(self, timestamp):
        self.timestamp = max(self.timestamp, timestamp) + 1

    def increment_timestamp(self):
        self.timestamp += 1

    def send_message(self, _to, _message):
        self.rpc_service.send_message(_to, _message)

    def run(self):
        self.worker.start()
        ThreadedServer(self.rpc_service, port=self.port).start()
