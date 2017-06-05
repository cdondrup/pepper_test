#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import naoqi_interfaces.comms.connection as con
from blue_peter.person_detection import PersonDetection
from naoqi_interfaces.utils.flow_control import Spinner
from blue_peter.animated_say import AnimatedSay
from blue_peter.posture import Posture
from blue_peter.motion import Motion
from blue_peter.dialogue import Dialogue

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="pepper",
                        help="Robot ip address")
    parser.add_argument("-p", "--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()

    broker = con.create_broker(args.ip, args.port)

    s = PersonDetection()
    m = Motion()
    a = AnimatedSay()
    p = Posture()
    d = Dialogue()

    p.stand()
    s.start(globals())
    m.start_breathing()
    d.start(globals())

    Spinner().spin()

    m.stop_breathing()
    p.stand()
    d.stop()
    s.stop()
    con.shutdown_broker(broker)
