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
import encoderDriver

class SwitchDriver:
    '''!
    '''
    def __init__(self, switchPin):
        '''!
        Creates an switch driver by initializing GPIO
        '''
        self.switchPin = pyb.Pin(switchPin, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
        
    def getValue(self):
        '''!
        Reads the limit switch
        @returns A boolean that is 0 when the switch is hit
        and 1 when the switch is not hit
        '''
        return self.switchPin.value()
        

