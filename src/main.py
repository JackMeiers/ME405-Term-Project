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

def task0_master ():
    """!
    Takes and converts GCode and passes to to program for drawing device
    """
    i = True
    while True:
        if i:
            for angle in range(0,20,1):
                print(angle)
                share_degree1.put(angle)
                share_degree2.put(angle)
                yield(0)
            i = False
        else:
            for angle in range(20,0,-1):
                print(angle)
                share_degree1.put(angle)
                share_degree2.put(angle)
                yield(0)
            i = True

def task1_encoder1 ():
    """!
    This task creates a driver for one of the encoders being used.
    It puts the curent value of the encoder into a share to be used by other tasks
    """
    switch = switchDriver.SwitchDriver(pyb.Pin.board.PC3)
    enc = encoderDriver.EncoderDriver(pyb.Pin.board.PB6,pyb.Pin.board.PB7, 4)
    while True:
        if not switch.getValue():
            print("PLEASE GOD NO 1")
            share_motor1.put(0)
            share_enc1.put(0)
            share_degree1.put(0)
        else:
            enc.update()
        share_enc1.put(enc.read())
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
    controller = controls.Controls(-16092, 1500/8192, 0)
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
    switch = switchDriver.SwitchDriver(pyb.Pin.board.PC2)
    enc = encoderDriver.EncoderDriver(pyb.Pin.board.PC6,pyb.Pin.board.PC7, 8)
    while True:
        if not switch.getValue():
            print("PLEASE GOD NO 2")
            share_motor2.put(0)
            share_enc2.put(0)
            share_degree2.put(0)
        else:
            enc.update()
        share_enc2.put(enc.read())
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
    controller = controls.Controls(16092, 1500/8192, 0)
    while True:
        controller.set_setpoint(encoderDriver.degree_to_enc(share_degree2.get(), (7/2)))
        share_motor2.put(controller.controlLoop(share_enc2.get()))
        yield(0)
    

"""! This main code creates multiple shares for the two motor duty cycles and encoder ticks.
     It then adds the tasks to cotask to be ran. The tasks run until somebody presses ENTER, at
     which time the scheduler stops and printouts show diagnostic information about the
     tasks and shares"""

if __name__ == "__main__":
    
    '''queue_enc1Values = task_share.Queue ('f', 16, thread_protect = False, overwrite = False,
                           name = "Enc Coordinates Queue 1")
    queue_enc2Values = task_share.Queue ('f', 16, thread_protect = False, overwrite = False,
                           name = "Enc Coordinates Queue 2")'''
    share_degree1 = task_share.Share ('f', thread_protect = False, name = "Share Degree 1")
    share_degree2 = task_share.Share ('f', thread_protect = False, name = "Share Degree 2")
    share_enc1 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 1")
    share_enc2 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 2")

    share_motor1 = task_share.Share ('f', thread_protect = False, name = "Share Motor 1")
    share_motor2 = task_share.Share ('f', thread_protect = False, name = "Share Motor 2")
    

    task0 = cotask.Task (task0_master, name = 'Master', priority = 4, 
                         period = 200, profile = True, trace = False)
    task1 = cotask.Task (task1_encoder1, name = 'Encoder1', priority = 2, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task2_motor1, name = 'Motor1', priority = 1, 
                         period = 6, profile = True, trace = False)
    task3 = cotask.Task (task3_control1, name = 'Controller1', priority = 1, 
                         period = 5, profile = True, trace = False)
    task4 = cotask.Task (task4_encoder2, name = 'Encoder2', priority = 2, 
                         period = 10, profile = True, trace = False)
    task5 = cotask.Task (task5_motor2, name = 'Motor2', priority = 1, 
                         period = 6, profile = True, trace = False)
    task6 = cotask.Task (task6_control2, name = 'Controller2', priority = 1, 
                         period = 5, profile = True, trace = False)
    
    cotask.task_list.append (task0)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)
    cotask.task_list.append (task3)
    cotask.task_list.append (task4)
    cotask.task_list.append (task5)
    cotask.task_list.append (task6)

   
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

