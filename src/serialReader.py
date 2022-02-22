"""!@file main.py
    This file contains all the funcitons printing out
    a graph of the encoder position to help us visualize
    the runtime nature of the motor
    @author Lucas Sandsor
    @author Jack Barone
    @author Jackson Myers
    @date 25-Jan-2022 
"""
from matplotlib import pyplot
import serial

def isnum(string):
    '''!Tries to convert a string to a number
        @param string    A string to be converted to a float
        @return    Returns a boolean that is true if the string
        can be converted to a number and false if it cannot
    '''
    try:
        float(string)
        return True
    except ValueError as e:
        return False
    
def serialHandler():
    '''!@brief A program to handle the serial input and output 
        @detail Program handles serial communication and prints
        a nice graph to visualize the runtime movement of the motor
        Sends a s for 'serial run', and then sends a c to stop the program
        get the encoder values and time over serial
    '''
    time_list = []
    tick_list = []
    with serial.Serial('COM4', 115200) as s_port:
        '''s_port.write(b's')
        s_port.write(b'\r')
        s_port.write(b'c')
        s_port.write(b'\r')'''
        for line in s_port:
            #manually sent EOF needed because serial port doesn't have EOF
            if b'EOF' in line:
                break
            if b',' in line:
                split_line = line.split(b',')
                for i in range(0,2,1):
                    split_line[i] = split_line[i].replace(b'\n', b'').strip()
                    split_line[i] = split_line[i].replace(b'\r', b'').strip()
                    if i == 0 and isnum(split_line[i]):
                        time_list.append(float(split_line[i]))
                    elif i == 1 and isnum(split_line[i]):
                        tick_list.append(float(split_line[i]))
    pyplot.plot(time_list,tick_list)
    pyplot.autumn()
    pyplot.ylabel("Ticks")
    pyplot.xlabel("Time")
    pyplot.show()
                        
if __name__ == "__main__":
    #Created serialHandler in case we want to impliment this function later
    serialHandler()

