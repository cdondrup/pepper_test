#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:47:54 2016

@author: cd32
"""

from __future__ import print_function

import time
import signal
import argparse
from naoqi import ALProxy, ALBroker, ALModule
import yaml
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
               "0.0.0.0",   # listen to anyone
               0,           # find a free port and use it
               ip,         # parent broker IP
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


class SpeechRecognitionTest(EventAbstractclass):
    EVENT_NAME = "WordRecognized"

    def __init__(self, filename, ip, port, language, word_spotting, audio, visual):
        super(self.__class__, self).__init__(self.__class__.__name__, ip, port)

        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

        self.asr = ALProxy("ALSpeechRecognition")
        print(self.asr.getAvailableLanguages())

        vocabulary = self.read_vocabulary(filename)
        print("Using vocabulary: %s" % vocabulary)
        self.configure(
            vocabulary=vocabulary,
            language=language,
            word_spotting=word_spotting,
            audio=audio,
            visual=visual
        )

        self.subscribe(
            event=SpeechRecognitionTest.EVENT_NAME,
            callback=self.callback
        )

        print("Subscribers:", self.memory.getSubscribers(SpeechRecognitionTest.EVENT_NAME))

        self._spin()

        self.unsubscribe(SpeechRecognitionTest.EVENT_NAME)
        self.broker.shutdown()

    def configure(self, vocabulary, word_spotting, language, audio, visual):
        self.asr.pause(True)
        self.asr.setVocabulary(vocabulary, word_spotting)
        self.asr.setLanguage(language)
        self.asr.setAudioExpression(audio)
        self.asr.setVisualExpression(visual)
        self.asr.pause(False)

    def callback(self, *args, **kwargs):
        print(args)
        print(kwargs)

    def read_vocabulary(self, f):
        with open(f, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as e:
                print(e)

    def _spin(self, *args):
        while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print('Caught Ctrl+C, stopping.')
        self.__shutdown_requested = True
        print('Good-bye')


if __name__ == "__main__":

    languages = ["English"]

    parser = argparse.ArgumentParser()
    parser.add_argument("vocabulary_file", type=str, help="A yaml file containing the list of words for the vocabulary.")
    parser.add_argument("-i", "--ip", type=str, default="pepper",
                        help="Robot ip address")
    parser.add_argument("-p", "--port", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("--language", type=str, default="English",
                        help="Use one of the supported languages: %s" % languages)
    parser.add_argument("--word-spotting", action="store_true",
                        help="Run in word spotting mode")
    parser.add_argument("--no-audio", action="store_true",
                        help="Turn off bip sound when recognition starts")
    parser.add_argument("--no-visual", action="store_true",
                        help="Turn off blinking eyes when recognition starts")
    args = parser.parse_args()

    if args.language in languages:
        s = SpeechRecognitionTest(
            filename=args.vocabulary_file,
            ip=args.ip,
            port=args.port,
            language=args.language,
            word_spotting=args.word_spotting,
            audio=not args.no_audio,
            visual=not args.no_visual
            )
    else:
        print("Unsupported language: '%s'. Please use -h to learn more." % args.language)
