from naoqi_interfaces.events.event_abstractclass import EventAbstractclass
from naoqi import ALProxy


class PersonDetection(EventAbstractclass):
    EVENT_NAME = "PeoplePerception/PeopleDetected"

    def __init__(self):
        super(self.__class__, self).__init__(inst=self, event=self.EVENT_NAME, proxy_name="ALPeoplePerception")
        self.create_proxy("ALTracker")
        self.tracking = -1
        self.ALTracker.setMode("Move")

    def callback(self, *args, **kwargs):
        min_distance = 1000.
        person_id = None
        for person in args[1][1]:
            if person[1] < min_distance:
                person_id = person[0]

        if person_id is not None:
            if self.tracking != person_id:
                print "Found person:", person_id
                self.ALTracker.stopTracker()
                self.ALTracker.removeAllTargets()
                print "Starting to track"
                self.tracking = person_id
                self.ALTracker.registerTarget("People", [self.tracking])
                self.ALTracker.track("People")

    def stop(self):
        super(self.__class__, self).stop()
        self.ALTracker.stopTracker()
        self.ALTracker.removeAllTargets()
