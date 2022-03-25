class EventObserver():
    def __init__(self):
        self.events = {}

    def subscribe(self, event_type, callback):
        self.events[event_type] = callback

    def notify(self, event_type, data):
        if event_type in self.events.keys():
            self.events[event_type](data)
