from naoqi_interfaces.events.multi_event_abstractclass import MultiEventAbstractclass
from naoqi import ALProxy


class PersonWordDetection(MultiEventAbstractclass):
    EVENT_NAME1 = "PeoplePerception/PeopleDetected"
    EVENT_NAME2 = "FaceDetected"

    def __init__(self):
        super(self.__class__, self).__init__(self, (self.EVENT_NAME1, self.EVENT_NAME2), (self.callback, self.callback2))
        self.proxies = [
            ALProxy("ALPeoplePerception"),
            ALProxy("ALFaceDetection")
            ]

    def callback(self, *args, **kwargs):
        print "PERSON"
        print args
        print kwargs

    def callback2(self, *args, **kwargs):
        print "FACE"
        print args
        print kwargs
