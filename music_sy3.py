# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 22:54:22 2020

@author: jzb
"""

import simpleaudio as sa
filename = 'myfile.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing