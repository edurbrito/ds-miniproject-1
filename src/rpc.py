from logging import exception

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
        return self.node.handle_message(_message)

    def send_message(self, _to, _message):
        try:
            conn = rpyc.connect("localhost", _to)
            conn._config['sync_request_timeout'] = 5
            response = conn.root.handle_message(self.port, _message)
            conn.close()
            return response
        except Exception as e:
            exception(e)
