from events.event_abstractclass import EventAbstractclass
from naoqi import ALProxy


class PersonDetection(EventAbstractclass):
    EVENT_NAME = "PeoplePerception/PeopleDetected"

    def __init__(self):
        super(self.__class__, self).__init__(self, self.EVENT_NAME)
        self.proxy = ALProxy("ALPeoplePerception")

    def callback(self, *args, **kwargs):
        print args
        print kwargs
