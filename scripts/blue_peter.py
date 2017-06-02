#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import comms.connection as con
from blue_peter.person_word_detection import PersonWordDetection
from utils.flow_control import Spinner

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", type=str, default="pepper",
                        help="Robot ip address")
    parser.add_argument("-p", "--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()

    broker = con.create_broker(args.ip, args.port)

    s = PersonWordDetection()
    s.start(globals())

    Spinner().spin()

    s.stop()
    con.shutdown_broker(broker)
