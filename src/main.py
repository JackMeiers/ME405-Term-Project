'''!
@file main.py
    This file contains a modified version of JR Ridgely's
    basic_task.py (https://github.com/spluttflob/ME405-Support)
    that creates tasks for running two seperate motors step responses at
    the same time
@author Lucas Sandsor
@author Jack Barone
@author Jack Meyers
@date 22-Feb-2022
'''

import gc
import pyb
import cotask
import task_share
import motorDriver
import encoderDriver
import controls
import utime
import switchDriver
import servoDriver
import kinematics
import gcode
from math import pi

def initialize_encoders():
    """!
    Initalizes the encoders to their respective positons
    """
    '''print("ENC1: ", share_enc1.get())
    print("ENC2: ", share_enc2.get())
    while share_enc1.get() < 0:
        cotask.task_list.pri_sched ()
        print("ENC1: ", share_enc1.get())
        share_motor1.put(-20)
        share_motor2.put(-20)
        utime.sleep_ms(500)
    while share_enc2.get() > 0:
        cotask.task_list.pri_sched ()
        print("ENC2: ", share_enc2.get())
        share_motor1.put(20)
        share_motor2.put(20)
        utime.sleep_ms(500)
    return True'''
    switch1 = switchDriver.SwitchDriver(pyb.Pin.board.PC2)
    enc1 = encoderDriver.EncoderDriver(pyb.Pin.board.PB6,pyb.Pin.board.PB7, 4)
    switch2 = switchDriver.SwitchDriver(pyb.Pin.board.PC3)
    enc2 = encoderDriver.EncoderDriver(pyb.Pin.board.PC6,pyb.Pin.board.PC7, 8)
    moe1 = motorDriver.MotorDriver(pyb.Pin.board.PA10,
        pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    moe2 = motorDriver.MotorDriver(pyb.Pin.board.PC1,
        pyb.Pin.board.PA0, pyb.Pin.board.A1, 5)
    while switch1.getValue():
        moe1.set_duty_cycle(60)
        moe2.set_duty_cycle(60)
        enc2.zero()
    print("SWITCH 2 DONE!")
    while switch2.getValue():
        moe1.set_duty_cycle(-60)
        moe2.set_duty_cycle(-60)
        enc1.zero()
    print("SWITCH 1 DONE!")
    i = 0
    while i < 2000:
        moe1.set_duty_cycle(60)
        moe2.set_duty_cycle(60)
        i = i + 1
        enc1.update()
        enc2.update()
    moe1.set_duty_cycle(0)
    moe2.set_duty_cycle(0)
    share_enc2.put(enc2.position)
    share_enc1.put(enc1.position)
    utime.sleep(5)
    


def task0_master ():
    """!
    Takes and converts GCode and passes to to program for drawing device
    """
    points = gcode.get_instructions("pentest.nc")
    while True:
        for point in points:
             #print("X-Y: ",end="")
             #print(gcode.apply_offset(point)[0],gcode.apply_offset(point)[1])
             angles = kinematics.convertToEncoderAngles(gcode.apply_offset(point)[0],gcode.apply_offset(point)[1])
             #print(angles[0] * 180 / pi, angles[1] * 180 / pi)
             share_degree1.put(angles[0] * 180 / pi)
             share_degree2.put(angles[1] * 180 / pi)
             share_servo.put(point[2])
             yield(0)

def task1_encoder1 ():
    """!
    This task creates a driver for one of the encoders being used.
    It puts the curent value of the encoder into a share to be used by other tasks
    """
    switch = switchDriver.SwitchDriver(pyb.Pin.board.PC2)
    enc = encoderDriver.EncoderDriver(pyb.Pin.board.PB6,pyb.Pin.board.PB7, 4)
    enc.position = share_enc1.get()
    while True:
        if not switch.getValue():
            print("OH THE HUMANITY!!!! 1")
            enc.zero()
            share_motor1.put(0)
            share_enc1.put(0)
            share_degree1.put(0)
        else:
            enc.update()
        share_enc1.put(enc.read())
        #print("ANGLE1: ", enc.position * (2/7) * 360/8192)
        yield (0)
        
def task2_motor1 ():
    """!
    This task creates a driver for one of the motors being used.
    It puts the current duty cycle of the motor into a share to be used by other tasks
    """
    moe = motorDriver.MotorDriver(pyb.Pin.board.PA10,
        pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    while True:
        moe.set_duty_cycle(share_motor1.get())
        yield(0)
        
def task3_control1 ():
    """!
    This task creates a controller for using the shared encoder
    value and uses it to adjust the speed of a motor to get to a desired position
    given by the user. It also stores the time and ticks of an encoder for outside
    analysis
    """
    #starts off at 5 degrees
    controller = controls.Controls(-16092, 5000/8192, 0)
    while True:
        controller.set_setpoint(-encoderDriver.degree_to_enc(share_degree1.get(), (7 / 2)))
        share_motor1.put(controller.controlLoop(share_enc1.get()))
        yield(0)

'''def task4_limitSwitch ():
    """!
    """
    switch = switchDriver(pyb.Pin.board.PC2)
    while True:
        if switch.getValue is True
            share_enc2.put(0)
        yield (0)
'''

def task4_encoder2 ():
    """!
    This task creates a driver for one of the encoders being used.
    It puts the curent value of the encoder into a share to be used by other tasks
    """
    switch = switchDriver.SwitchDriver(pyb.Pin.board.PC3)
    enc = encoderDriver.EncoderDriver(pyb.Pin.board.PC6,pyb.Pin.board.PC7, 8)
    enc.position = share_enc2.get()
    while True:
        if not switch.getValue():
            print("PLEASE OH GOD NO 2")
            enc.zero()
            share_motor2.put(0)
            share_enc2.put(0)
            share_degree2.put(0)
        else:
            enc.update()
        share_enc2.put(enc.read())
        #print("ANGLE2: ", enc.position * (2/7) * 360/8192)
        yield (0)
        
def task5_motor2 ():
    """!
    This task creates a driver for one of the motors being used.
    It puts the current duty cycle of the motor into a share to be used by other tasks
    """
    moe = motorDriver.MotorDriver(pyb.Pin.board.PC1,
        pyb.Pin.board.PA0, pyb.Pin.board.A1, 5)
    while True:
        moe.set_duty_cycle(share_motor2.get())
        yield(0)
        
def task6_control2 ():
    """!
    This task creates a controller for using the shared encoder
    value and uses it to adjust the speed of a motor to get to a desired position
    given by the user. It also stores the time and ticks of an encoder for outside
    analysis
    """
    #starts off at 5 degrees
    controller = controls.Controls(16092, 5000/8192, 0)
    while True:
        controller.set_setpoint(encoderDriver.degree_to_enc(share_degree2.get(), (7/2)))
        share_motor2.put(controller.controlLoop(share_enc2.get()))
        yield(0)
        
def task7_servo ():
    """!
    This task creates a controller for using the shared encoder
    value and uses it to adjust the speed of a motor to get to a desired position
    given by the user. It also stores the time and ticks of an encoder for outside
    analysis
    """
    #starts off at 5 degrees
    servo = servoDriver.ServoDriver(pyb.Pin.board.PA1, 2)
    while True:
        servo.set_duty_cycle(share_servo.get())
        yield(0)
    

"""! This main code creates multiple shares for the two motor duty cycles and encoder ticks.
     It then adds the tasks to cotask to be ran. The tasks run until somebody presses ENTER, at
     which time the scheduler stops and printouts show diagnostic information about the
     tasks and shares"""

if __name__ == "__main__":
    
    share_servo = task_share.Share ('i', thread_protect = False, name = "Share Servo")

    
    share_degree1 = task_share.Share ('f', thread_protect = False, name = "Share Degree 1")
    share_degree2 = task_share.Share ('f', thread_protect = False, name = "Share Degree 2")
    share_enc1 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 1")
    share_enc2 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 2")

    share_motor1 = task_share.Share ('f', thread_protect = False, name = "Share Motor 1")
    share_motor2 = task_share.Share ('f', thread_protect = False, name = "Share Motor 2")
    
    
    
    #
    #initialize_encoders()
    #
    
    #for approx hourglass y offset = + 15 feed 5000, master period 25 enc period 10, motor 6, control 1
    task0 = cotask.Task (task0_master, name = 'Master', priority = 4, 
                         period = 45, profile = True, trace = False)
    task1 = cotask.Task (task1_encoder1, name = 'Encoder1', priority = 2, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task2_motor1, name = 'Motor1', priority = 1, 
                         period = 6, profile = True, trace = False)
    task3 = cotask.Task (task3_control1, name = 'Controller1', priority = 1, 
                         period = 1, profile = True, trace = False)
    task4 = cotask.Task (task4_encoder2, name = 'Encoder2', priority = 2, 
                         period = 10, profile = True, trace = False)
    task5 = cotask.Task (task5_motor2, name = 'Motor2', priority = 1, 
                         period = 6, profile = True, trace = False)
    task6 = cotask.Task (task6_control2, name = 'Controller2', priority = 1, 
                         period = 1, profile = True, trace = False)
    task7 = cotask.Task (task7_servo, name = 'Servo', priority = 5, 
                         period = 100, profile = True, trace = False)
    
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task4)
    cotask.task_list.append (task5)

    
    '''initialized = False
    share_enc1.put(-8192)
    share_enc2.put(8192)
    while not initialized:
        cotask.task_list.pri_sched ()
        initialized = initialize_encoders()
        print("\n\n\n\nINITIALIZED\n\n\n")'''
    
    cotask.task_list.append (task0)
    cotask.task_list.append (task3)
    cotask.task_list.append (task6)
    cotask.task_list.append (task7)

    gc.collect ()

    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    

    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')

