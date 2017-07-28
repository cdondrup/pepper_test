#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from blue_peter.person_detection import PersonDetection
from naoqi_interfaces.control.event_manager import EventManager
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

    s = PersonDetection(
        event="PeoplePerception/PeopleDetected",
        proxy_name="ALPeoplePerception"
    )
    d = Dialogue(
        event="MyEventData",
        proxy_name="ALSpeechRecognition"
    )

    man = EventManager(
        globals_=globals(),
        ip=args.ip,
        port=args.port,
        events=[(s, ["WholeBody"]), (d, [YamlParser(args.config_file)])]
    )

    m = Motion()
    p = Posture()

    p.stand()
    m.start_breathing()

    man.on_shutdown(m.stop_breathing)
    man.on_shutdown(p.stand)
    man.spin()
