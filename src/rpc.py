
from logging import CRITICAL, DEBUG, ERROR, INFO, info, exception

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

    def exposed_handle_message(self, _from, _message):
        with self.node.lock:
            self.node.handle_message(_message)
            info(msg=f"RECEIVED FROM {_from} TO {self.port}")

    def exposed_handle_response(self, _from, _response):
        with self.node.lock:
            self.node.handle_response(_from, _response)
            info(
                msg=f"RESPONSE {_response} RECEIVED FROM {_from} TO {self.port}")

    def send_message(self, _to, _message):
        try:
            conn = rpyc.connect("localhost", _to)
            info(msg=f"SENT FROM {self.port} TO {_to}")
            conn.root.handle_message(self.port, _message)
            conn.close()
        except:
            info(msg=f"NOT SENT FROM {self.port} TO {_to}")

    def respond(self, _to, _response):
        try:
            conn = rpyc.connect("localhost", _to)
            info(msg=f"RESPONSE {_response} SENT FROM {self.port} TO {_to}")
            conn.root.handle_response(self.port, _response)
            conn.close()
        except Exception as e:
            info(
                msg=f"RESPONSE {_response} WAS NOT SENT FROM {self.port} TO {_to}")
            exception(e)
