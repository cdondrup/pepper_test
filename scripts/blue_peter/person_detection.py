from naoqi_interfaces.events.event_abstractclass import EventAbstractclass


class PersonDetection(EventAbstractclass):
    tracking_modes = ["Head", "WholeBody", "Move", "Navigate"]

    def init(self, *args):
        self.create_proxy("ALTracker")
        self.tracking = -1
        if args[0] not in self.tracking_modes:
            raise AttributeError("Unknown tracking mode '%s'" % tracking_mode)
        self.ALTracker.setMode(args[0])

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
