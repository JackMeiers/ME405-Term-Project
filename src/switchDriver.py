'''!
@file encoderDriver.py
This file contains all driver functions for the encoder by scanning
ticks of the encoder
@author Lucas Sandsor
@author Jack Barone
@author Jackson Myers
@date 22-Feb-2022 
'''
import pyb
class switchDriver:
    '''!
    '''
    def __init__(self, switchPin)
        '''!
        Creates an switch driver by initializing GPIO
        '''
        self.period = 4000 - 1
        self.pinSwitchPin = pyb.Pin (switchPin, pyb.Pin.IN, )        
        self.tim = pyb.Timer (timer, prescaler=0, freq=20000)
        self.ch1 = self.tim.channel (1, pyb.Timer.ENC_A, pin=self.pinIN1)
        self.ch2 = self.tim.channel (2, pyb.Timer.ENC_B, pin=self.pinIN2)
        self.count = 0
        self.lastCount = 0
        self.position = 0
        self.delta = 0


    