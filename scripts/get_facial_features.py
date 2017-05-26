#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import time
import sys
import argparse
from naoqi import ALBroker, ALProxy, ALModule
from abc import ABCMeta


class EventAbstractclass(ALModule):
    __metaclass__ = ABCMeta

    def __init__(self, name, ip, port):
        self.name = name
        self._make_global(self.name, self)
        self.broker = self._connect(ip, port)
        super(EventAbstractclass, self).__init__(self.name)

        self.memory = self._make_global("memory", ALProxy("ALMemory"))

    def _connect(self, ip, port):
        try:
            broker = ALBroker("speech_broker",
                              "0.0.0.0",  # listen to anyone
                              0,  # find a free port and use it
                              ip,  # parent broker IP
                              port)
            print("Connected to %s:%s" % (ip, str(port)))
            return broker
        except RuntimeError:
            print("Cannot connect to %s:%s. Retrying in 1 second." % (ip, str(port)))
            time.sleep(1)
            return self._connect(ip, port)

    def _make_global(self, name, var):
        globals()[name] = var
        return globals()[name]

    def subscribe(self, event, callback):
        print callback.func_name
        self.memory.subscribeToEvent(
            event,
            self.name,
            callback.func_name
        )

    def unsubscribe(self, event):
        self.memory.unsubscribeToEvent(
            event,
            self.name
        )

    def remove_subscribers(self, event):
        subscribers = self.memory.getSubscribers(event)
        if subscribers:
            print("Speech recognition already in use by another node")
            for module in subscribers:
                self.__stop_module(module, event)

    def __stop_module(self, module, event):
        print("Unsubscribing '{}' from NAO speech recognition".format(
            module))
        try:
            self.memory.unsubscribeToEvent(event, module)
        except RuntimeError:
            print("Could not unsubscribe from NAO speech recognition")


class HumanGreeter(EventAbstractclass):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, ip, port):
        """
        Initialisation of qi framework and event detection.
        """
        super(self.__class__, self).__init__(self.__class__.__name__, ip, port)
        # Get the service ALMemory.
        # Connect the event callback.
        self.got_face = False
        self.tts = ALProxy("ALTextToSpeech")
        self.face_detection = ALProxy("ALFaceDetection")

        self.subscribe(
            event="FaceDetected",
            callback=self.on_human_tracked
        )

        print "Subscribers:", self.memory.getSubscribers("FaceDetected")
        print "Globals", globals()
        # Get the services ALTextToSpeech and ALFaceDetection.

    def on_human_tracked(self, *args, **kwargs):
        """
        Callback for event FaceDetected.
        """
        print(args)
        print(kwargs)
        # if value == []:  # empty value when the face disappears
        #     self.got_face = False
        # elif not self.got_face:  # only speak the first time a face appears
        # self.got_face = True
        # print "I saw a face!"
        # # self.tts.say("Hello, you!")
        # # First Field = TimeStamp.
        # print "Value:", value
        # timeStamp = value[0]
        # print "TimeStamp is: " + str(timeStamp)
        #
        # # Second Field = array of face_Info's.
        # faceInfoArray = value[1]
        # for j in range(len(faceInfoArray) - 1):
        #     faceInfo = faceInfoArray[j]
        #
        #     # First Field = Shape info.
        #     faceShapeInfo = faceInfo[0]
        #
        #     # Second Field = Extra info (empty for now).
        #     faceExtraInfo = faceInfo[1]
        #
        #     print "Face Infos :  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
        #     print "Face Infos :  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
        #     print "Face Extra Infos :" + str(faceExtraInfo)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            # stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    # try:
    #     # Initialize qi framework.
    #     connection_url = "tcp://" + args.ip + ":" + str(args.port)
    #     app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    # except RuntimeError:
    #     print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
    #            "Please check your script arguments. Run with -h option for help.")
    #     sys.exit(1)

    human_greeter = HumanGreeter(args.ip, args.port)
    human_greeter.run()
