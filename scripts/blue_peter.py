#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import naoqi_interfaces.comms.connection as con
from blue_peter.person_detection import PersonDetection
from naoqi_interfaces.control.event_spinner import EventSpinner
from blue_peter.animated_say import AnimatedSay
from blue_peter.posture import Posture
from blue_peter.motion import Motion
from blue_peter.dialogue import Dialogue
from blue_peter.yaml_parser import YamlParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", type=str,
                        help="A yaml file containing the config to be used.")
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
    d = Dialogue(YamlParser(args.config_file))

    p.stand()
    m.start_breathing()

    spinner = EventSpinner(
        globals_=globals(),
        broker=broker,
        events=[s, d]
    )
    spinner.spin()

    m.stop_breathing,
    p.stand
