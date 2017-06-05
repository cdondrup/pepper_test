from naoqi_interfaces.events.event_abstractclass import EventAbstractclass


class Tracking(EventAbstractclass):
    EVENT_NAME = "FaceDetected"

    def __init__(self):
        super(self.__class__, self).__init__(inst=self, event=self.EVENT_NAME, proxy_name="ALFaceDetection")
        self.ALFaceDetection.setTrackingEnabled(True)

    def callback(self, *args, **kwargs):
        pass

    def start(self, glob):
        super(self.__class__, self).start(glob)
        self.ALFaceDetection.setTrackingEnabled(True)

    def stop(self):
        super(self.__class__, self).stop()
        self.ALFaceDetection.setTrackingEnabled(False)
