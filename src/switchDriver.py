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

class switchDriver:
    '''!
    '''
    def __init__(self, switchPin)
        '''!
        Creates an switch driver by initializing GPIO
        '''
        self.pinSwitchPin = pyb.Pin(switchPin, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
     
    def getValue(self)
        '''!
        Reads the limit switch
        @returns A boolean that is true when the switch is hit
        and false when the switch is not hit
        '''
        return pinSwitchPin.value()
        


    