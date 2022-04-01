import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
from critical_section import CriticalSection
from process import Process
from event_observer import EventObserver
from __env__ import *


class MonitorService(rpyc.Service):
    ALIASES = ["DS-MINIPROJECT-1"]

    def __init__(self) -> None:
        super().__init__()
        self.critical_section = CriticalSection()
        self.processes = {}
        self.event_observer = EventObserver()
        self.event_observer.subscribe('onSetWantedState', self.request_access)
        self.event_observer.subscribe('onRelease', self.handle_queued_processes)

    def get_event_time(self, event):
        return "{} on {}".format(event, datetime.datetime.now())

    def on_connect(self, conn):
        print(self.get_event_time("connected"))

    def on_disconnect(self, conn):
        print(self.get_event_time("disconnected"))

    def exposed_start(self, N):
        for i in range(1, int(N)+1):
            p = Process(i, self.event_observer)
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
            return f"Timeout interval for CS changed to [{10}, {t}]."
        return "Invalid t"

    def exposed_time_p(self, t):
        if t >= 5:
            for p in self.processes:
                self.processes[p].set_timeout(t)
            return f"Timeout interval for processes changed [{5}, {t}]."
        return "Invalid t"
    
    def request_access(self, id):
        sender = self.processes[id]

        for key, value in self.processes.items():
            sender.timestamp += 1
            if key != id:
                reply = value.handle_message((sender.timestamp, id))
                sender.replies[key] = reply

        self.check_replies(sender)

    def check_replies(self, process):
        if all(process.replies.values()):
            process.state = HELD
            self.critical_section.assign_process(process)
            process.replies = {}

    def handle_queued_processes(self, data):
        queue, releaser_id = data
        while len(queue) != 0:
            sender = self.processes[releaser_id]
            sender.timestamp += 1

            _, id = queue.pop(0)

            receiver = self.processes[id]
            receiver.replies[releaser_id] = "OK"
            receiver.adjust_timestamp(sender.timestamp)

            self.check_replies(receiver)



if __name__ == '__main__':
    t = ThreadedServer(MonitorService, port=18812)
    t.start()
