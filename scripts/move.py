#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:18:12 2016

@author: cdondrup
"""
import time
import argparse
from naoqi import ALProxy


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class KeyBoardTeleOp(object):
    __kill_key = 'k'
    def __init__(self, robot_ip, port):
        self.robot_ip = robot_ip
        self.port = port
        self.connect(robot_ip, port)
        self.vels = {
            'x': {'current': .0, 'min': -.55, 'max': .55},
            'y': {'current': .0, 'min': -.55, 'max': .55},
            't': {'current': .0, 'min': -1., 'max': 1.}
        }

    def connect(self, robot_ip, port):
        try:
            self.motion_proxy  = ALProxy("ALMotion", robot_ip, port)
            self.basic_awareness_proxy = ALProxy("ALBasicAwareness", robot_ip, port)
            print "Connected to %s:%s" % (robot_ip, str(port))
        except RuntimeError:
            print "Cannot connect to %s:%s. Retrying in 1 second." % (robot_ip, str(port))
            time.sleep(1)
            self.connect(robot_ip, port)

    def spin(self):
        getch = _Getch()
        ch = None
        print "Turning off basic awareness"
        self.awareness_mode = self.basic_awareness_proxy.getEngagementMode()
        self.tracking_mode = self.basic_awareness_proxy.getTrackingMode()
        self.basic_awareness_proxy.stopAwareness()
        print "Waiting for key"
        while ch != self.__kill_key:
            ch = getch()
            if ch == 'w':
                if self.vels['x']['current'] + 0.05 < self.vels['x']['max']:
                    self.vels['x']['current'] += 0.05
                else:
                    self.vels['x']['current'] = self.vels['x']['max']
            elif ch == 's':
                if self.vels['x']['current'] - 0.05 > self.vels['x']['min']:
                    self.vels['x']['current'] -= 0.05
                else:
                    self.vels['x']['current'] = self.vels['x']['min']
            elif ch == 'q':
                if self.vels['y']['current'] + 0.05 < self.vels['y']['max']:
                    self.vels['y']['current'] += 0.05
                else:
                    self.vels['y']['current'] = self.vels['y']['max']
            elif ch == 'e':
                if self.vels['y']['current'] - 0.05 > self.vels['y']['min']:
                    self.vels['y']['current'] -= 0.05
                else:
                    self.vels['y']['current'] = self.vels['y']['min']
            elif ch == 'a':
                if self.vels['t']['current'] + 0.1 < self.vels['t']['max']:
                    self.vels['t']['current'] += 0.1
                else:
                    self.vels['t']['current'] = self.vels['t']['max']
            elif ch == 'd':
                if self.vels['t']['current'] - 0.1 > self.vels['t']['min']:
                    self.vels['t']['current'] -= 0.1
                else:
                    self.vels['t']['current'] = self.vels['t']['min']
            elif ch == ' ':
                self.vels['x']['current'] = 0.0
                self.vels['y']['current'] = 0.0
                self.vels['t']['current'] = 0.0

            command = {}
            for k,v in self.vels.items():
                command[k] = round(v['current'],2)
            self._move(**command)
            if ch != self.__kill_key: print command

        print "Starting basic awareness with %s and %s" % (self.awareness_mode, self.tracking_mode)
        self.motion_proxy.wakeUp()
        self.basic_awareness_proxy.setEngagementMode(self.awareness_mode)
        self.basic_awareness_proxy.setTrackingMode(self.tracking_mode)
        self.basic_awareness_proxy.startAwareness()

        print "Good-bye"
        self._stop()

    def _stop(self):
        self._move()

    def _move(self, x=.0, y=.0, t=.0):
        self.motion_proxy.post.move(x, y, t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.37",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")
    args = parser.parse_args()

    k = KeyBoardTeleOp(args.ip, args.port)
    k.spin()
