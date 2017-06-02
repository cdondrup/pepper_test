#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: cdondrup
"""

import numpy
import wave
import argparse
import struct
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api


class NoiseReduction(object):
    def __init__(self, filename):
        print "Opening:", filename
        wave_file = wave.open(filename, 'r')
        print wave_file.getnchannels()
        length = wave_file.getnframes()
        for i in range(0, length):
            wave_data = wave_file.readframes(1)
            data = struct.unpack("<h", wave_data)
            # print(int(data[0]))
        wave_file.close()
        fs, data = wavfile.read(filename)  # load the data
        print fs
        print data
        a = data.T  # this is a two channel soundtrack, I get the first track
        b = [(ele / 2 ** 8.) * 2 - 1 for ele in a]  # this is 8-bit track, b is now normalized on [-1,1)
        c = fft(b)  # calculate fourier transform (complex numbers list)
        d = len(c) / 2  # you only need half of the fft list (real signal symmetry)
        plt.plot(abs(c[:(d - 1)]), 'r')
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str,
                        help="The output file name on the robot. Please use home dir: /home/nao/")
    args = parser.parse_args()

    n = NoiseReduction(args.file_name)
