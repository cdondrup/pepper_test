from naoqi import ALProxy, ALModule
from abc import ABCMeta, abstractmethod


class EventAbstractclass(ALModule):
    __metaclass__ = ABCMeta

    def __init__(self, inst, event):
        self.inst = inst
        self.event = event
        self.name = inst.__class__.__name__+"_inst"
        self._make_global(self.name, self)
        super(EventAbstractclass, self).__init__(self.name)

        self.memory = self._make_global("memory", ALProxy("ALMemory"))

    def _make_global(self, name, var):
        globals()[name] = var
        return globals()[name]

    def _subscribe(self):
        self.memory.subscribeToEvent(
            self.event,
            self.name,
            self.callback.func_name
        )

    def _unsubscribe(self):
        self.memory.unsubscribeToEvent(
            self.event,
            self.name
        )

    def sync_global(self, glob):
        glob[self.name] = globals()[self.name]

    @abstractmethod
    def callback(self, *args, **kwargs):
        """
        This function is called whenever the event fires and needs to be overridden
        
        :param args: 
        :param kwargs: 
        """
        pass

    def start(self, glob):
        """
        Subscribes to the event and syncs the necessary globals.
        :param glob: The globals() of the main file
        :return: 
        """
        self.sync_global(glob)
        self._subscribe()

    def stop(self):
        """
        Unsubscribes from event 
        """
        self._unsubscribe()
