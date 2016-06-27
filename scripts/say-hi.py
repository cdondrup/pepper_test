#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 14:25:30 2016

@author: cdondrup
"""

from naoqi import ALProxy, ALBroker, ALModule
import time
import sys

ip_robot = "192.168.1.37"
port_robot = 9559


# Global variable to store the humanEventWatcher module instance
humanEventWatcher = None
memory = None


class HumanTrackedEventWatcher(ALModule):
    """ A module to react to HumanTracked and PeopleLeft events """

    def __init__(self):
        ALModule.__init__(self, "humanEventWatcher")
        global memory
        memory = ALProxy("ALMemory", ip_robot, port_robot)
        memory.subscribeToEvent("ALBasicAwareness/HumanTracked",
                                "humanEventWatcher",
                                "onHumanTracked")
        memory.subscribeToEvent("ALBasicAwareness/PeopleLeft",
                                "humanEventWatcher",
                                "onPeopleLeft")
        self.tts = ALProxy("ALTextToSpeech", ip_robot, port_robot)

    def onHumanTracked(self, key, value, msg):
        """ callback for event HumanTracked """
        print "got HumanTracked: detected person with ID:", str(value)
        if value >= 0:  # found a new person
            animated_tts.say("hello, I am pepper.")
            position_human = self.get_people_perception_data(value)
            [x, y, z] = position_human
            print "The tracked person with ID", value, "is at the position:", \
                "x=", x, "/ y=",  y, "/ z=", z

    def onPeopleLeft(self, key, value, msg):
        """ callback for event PeopleLeft """
        print "got PeopleLeft: lost person", str(value)
        self.stop_speech_reco()

    def get_people_perception_data(self, id_person_tracked):
        memory = ALProxy("ALMemory", ip_robot, port_robot)
        memory_key = "PeoplePerception/Person/" + str(id_person_tracked) + \
                     "/PositionInWorldFrame"
        return memory.getData(memory_key)


if __name__ == "__main__":
    event_broker = ALBroker("event_broker", "0.0.0.0", 0,
                            ip_robot, port_robot)
    global humanEventWatcher
    humanEventWatcher = HumanTrackedEventWatcher()
    basic_awareness = ALProxy("ALBasicAwareness", ip_robot, port_robot)
    motion = ALProxy("ALMotion", ip_robot, port_robot)
    animated_tts = ALProxy("ALAnimatedSpeech", ip_robot, port_robot)
    ttw = {"hello_tag": ["hello", "hey", "hi"]}    
    tfa = {"hello_tag": ["animations/Stand/Gesture/Hey_1"]}
    configuration = {"bodyLanguageMode": "contextual"}
#    animated_tts.addTagsToWords(ttw)
#    animated_tts.declareTagForAnimations(tfa)

    #start
#    motion.wakeUp()
#    basic_awareness.setEngagementMode("FullyEngaged")
#    basic_awareness.startAwareness()

    #loop on, wait for events until interruption
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        #stop
#        basic_awareness.stopAwareness()
#        motion.rest()
        event_broker.shutdown()
        sys.exit(0)