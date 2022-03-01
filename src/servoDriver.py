'''!
@file servoDriver.py
File contains the necessary code to enable and run a motor using PWM.
Pin numbers and timer are parameterized so multiple motors can be run at the same time.
@author Lucas Sandsor
@author Jack Barone
@author Jack Meyers
@date 27-Feb-2022
'''

import pyb
class ServoDriver:
    '''!
    This class impliments a servo driver for ME405
    '''
    def __init__ (self, in1pin, timer):
        '''!
        Creates a servo driver
        @param in1pin Input pin 1 for driving the motor forwards
        @param timer The number of the timer to use (channels 1 and 2) 
        '''
        #print("Creating a motor driver")
        self.pinIN1 = pyb.Pin (in1pin, pyb.Pin.OUT_PP)
        #must declare pyb.Pin.board.en_pin in main
        self.tim = pyb.Timer (timer, freq=50)
        self.ch1 = self.tim.channel (1, pyb.Timer.PWM, pin=self.pinIN1)
        
    def set_duty_cycle(self, level):
        '''!
        This method sets duty cycle of motor to a certain
        level. Positive cuase torque in one direction and
        negative causes torque in another
        If the duty cycle is out of the acceptable range, it
        will prin
        @param level The duty cycle level to run the motor at (-100 to 100)
        '''
        if(level > 100):
            #print ('Setting duty cycle to ' + str (100))
            self.ch1.pulse_width_percent (100)
        elif(level < 0):
            #print ('Setting duty cycle to ' + str (-100))
            self.ch1.pulse_width_percent (0)
        else:
            self.ch1.pulse_width_percent (abs(level))
                
                