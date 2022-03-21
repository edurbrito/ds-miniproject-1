class CriticalSection():
    def __init__(self) -> None:
        self.process = None
        self.timeout = 10, 10  # min, max
        # maybe some queue for the processes based on their timestamp

    def set_timeout(self, t):
        if t >= 10:
            self.timeout = 10, t

    def assign_process(self, process):
        self.process = process
