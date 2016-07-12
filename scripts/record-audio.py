#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:18:12 2016

@author: cdondrup
"""
import time
import signal
import argparse
from naoqi import ALProxy


class RecordAudio(object):
    def __init__(self, robot_ip, port):
        self.connect(robot_ip, port)

    def connect(self, robot_ip, port):
        try:
            self.recorder  = ALProxy("ALAudioRecorder", robot_ip, port)
            print "Connected to %s:%s" % (robot_ip, str(port))
        except RuntimeError:
            print "Cannot connect to %s:%s. Retrying in 1 second." % (robot_ip, str(port))
            time.sleep(1)
            self.connect(robot_ip, port)

    def record(self, f, t):
        channels = [1,1,1,1] # Left, right, front, rear
        samplingrate = 48000 # 4 channels=48000, 1 channel=16000
        self.recorder.startMicrophonesRecording(f, t, samplingrate, channels)
        print "Started recording. Please pres Ctrl+C to stop recording."

    def signal_handler(self, signal, frame):
        print('Caught Ctrl+C, stopping to record.')
        self.recorder.stopMicrophonesRecording()
        print('Recording stopped. Good-bye')


if __name__ == "__main__":
    types = ["wav", "ogg"]

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, help="The output file name on the robot. Please use home dir: /home/nao/")
    parser.add_argument("--ip", type=str, default="pepper",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--type", type=str, default="wav",
                        help="The target encoding. Choose from: " + ', '.join(types))
    args = parser.parse_args()

    if args.type in types:
        r = RecordAudio(args.ip, args.port)
        r.record(args.file_name, args.type)
        signal.signal(signal.SIGINT, r.signal_handler)
    else:
        print "### Unknown data type: %s. Please choose from:" % args.type, ', '.join(types)

    signal.pause()
