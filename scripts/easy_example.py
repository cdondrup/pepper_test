#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

from naoqi import ALModule, ALProxy, ALBroker
import argparse
import sys
import time


class GetFaceData(ALModule): #Create a class that inherits from ALModule
    def __init__(self):
        super(GetFaceData, self).__init__("get_face_data") # Call constructor of ALModule with name of global variable
        self.face_detection = ALProxy("ALFaceDetection") # Need to create this so it is running on the robot
        memory.subscribeToEvent("FaceDetected", "get_face_data", "callback") # Name of event, name of instance of class, name of callback function

    def callback(self, event, value, subscriberIdentifier):
        print event, value, subscriberIdentifier

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
            sys.exit(0)


parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="127.0.0.1",
                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=9559,
                    help="Naoqi port number")

args = parser.parse_args()

try:
    broker = ALBroker("face_recognition",
                      "0.0.0.0",  # listen to anyone
                      0,  # find a free port and use it
                      args.ip,  # parent broker IP
                      args.port)
    print "Connected to %s:%s" % (args.ip, str(args.port))
except RuntimeError:
    print "Cannot connect to %s:%s. Retrying in 1 second." % (args.ip, str(args.port))
    sys.exit(1)

memory = ALProxy("ALMemory") # Memory has to be global
get_face_data = GetFaceData() # Global variable for class instance
get_face_data.run() # Keeping it alive
