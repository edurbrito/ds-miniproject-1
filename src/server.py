import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
from critical_section import CriticalSection
from process import Process


class MonitorService(rpyc.Service):
    ALIASES = ["DS-MINIPROJECT-1"]

    def __init__(self) -> None:
        super().__init__()
        self.critical_section = CriticalSection()
        self.processes = {}

    def get_event_time(self, event):
        return "{} on {}".format(event, datetime.datetime.now())

    def on_connect(self, conn):
        print(self.get_event_time("connected"))

    def on_disconnect(self, conn):
        print(self.get_event_time("disconnected"))

    def exposed_start(self, N):
        for i in range(1, int(N)+1):
            p = Process(i)
            p.start()
            self.processes[i] = p

    def exposed_list(self):
        result = []
        for p in self.processes:
            result.append(str(self.processes[p]))
        return "\n".join(result)

    def exposed_time_cs(self, t):
        if t >= 10:
            self.critical_section.set_timeout(t)
            return f"Timeout for CS changed to [{10}, {t}]."
        return "Invalid t"

    def exposed_time_p(self, t):
        if t >= 5:
            for p in self.processes:
                self.processes[p].set_timeout(t)
            return f"Timeout for CS changed [{5}, {t}]."
        return "Invalid t"


if __name__ == '__main__':
    t = ThreadedServer(MonitorService, port=18812)
    t.start()
