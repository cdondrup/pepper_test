#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:21:25 2016

@author: cdondrup
"""

import time
import argparse
from naoqi import ALProxy


class EngagmentMode(object):
    def __init__(self, robot_ip, port):
        self.robot_ip = robot_ip
        self.port = port
        self.connect(robot_ip, port)
        
    def connect(self, robot_ip, port):
        try:
            self.motion_proxy  = ALProxy("ALMotion", robot_ip, port)
            self.basic_awareness_proxy = ALProxy("ALBasicAwareness", robot_ip, port)
            print "Connected to %s:%s" % (robot_ip, str(port))
        except RuntimeError:
            print "Cannot connect to %s:%s. Retrying in 1 second." % (robot_ip, str(port))
            time.sleep(1)
            self.connect(robot_ip, port)
            
    def set_mode(self, awareness_mode, tracking_mode):
        print "Stopping awareness"
        self.basic_awareness_proxy.stopAwareness()
        print "Setting new awareness mode: %s with %s" % (awareness_mode, tracking_mode)
        self.motion_proxy.wakeUp()
        self.basic_awareness_proxy.setEngagementMode(awareness_mode)
        self.basic_awareness_proxy.setTrackingMode(tracking_mode)
        self.basic_awareness_proxy.startAwareness()

if __name__ == "__main__":
    awareness_modes = ["Unengaged", "SemiEngaged", "FullyEngaged"] 
    tracking_modes = ["Head", "BodyRotation", "WholeBody", "MoveContextually"] 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.37",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("awareness_mode", type=str, default="SemiEngaged",
                        help="Choose from " + ', '.join(awareness_modes))
    parser.add_argument("tracking_mode", type=str, default="BodyRotation",
                        help="Choose from " + ', '.join(tracking_modes))
    args = parser.parse_args()

    if args.awareness_mode in awareness_modes:
        if args.tracking_mode in tracking_modes:
            e = EngagmentMode(args.ip, args.port)
            e.set_mode(args.awareness_mode, args.tracking_mode)
        else:
            print args.tracking_mode + "is unknown."
    else:
        print args.awareness_mode + "is unknown."

