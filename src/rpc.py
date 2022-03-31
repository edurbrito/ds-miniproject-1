
from logging import CRITICAL, DEBUG, ERROR, INFO, info

import rpyc


class RPCService(rpyc.Service):
    ALIASES = []

    def __init__(self, node) -> None:
        self.node = node
        self.port = self.node.port
        self.ALIASES.append(f"process-{self.port}")
        super().__init__()

    def exposed_get_state(self):
        return str(self.node)

    def exposed_set_timeout_cs(self, t):
        return bool(self.node.set_timeout_cs(t))

    def exposed_set_timeout_p(self, t):
        return bool(self.node.set_timeout_p(t))

    def exposed_deliver_message(self, _from, _message):
        with self.node.lock:
            self.node.queue.append(f"{_from} : {_message}")
            info(msg=f"RECEIVED FROM {_from} TO {self.port}")

    def send_message(self, _to, _message):
        try:
            conn = rpyc.connect("localhost", _to)
            conn.root.deliver_message(self.port, _message)
            conn.close()
            info(msg=f"SENT FROM {self.port} TO {_to}")
        except:
            info(msg=f"NOT SENT FROM {self.port} TO {_to}")
