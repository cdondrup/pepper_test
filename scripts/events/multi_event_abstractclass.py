from event_abstractclass import EventAbstractclass
from abc import ABCMeta, abstractmethod


class MultiEventAbstractclass(EventAbstractclass):
    __metaclass__ = ABCMeta

    def __init__(self, inst, events, callbacks):
        super(MultiEventAbstractclass, self).__init__(inst, None)
        self.events = events
        self.callbacks = callbacks

    def _subscribe(self):
        for e, c in zip(self.events, self.callbacks):
            self.memory.subscribeToEvent(
                e,
                self.name,
                c.func_name
            )

    def _unsubscribe(self):
        for e in self.events:
            self.memory.unsubscribeToEvent(
                e,
                self.name
            )

    def callback(self, *args, **kwargs):
        return
