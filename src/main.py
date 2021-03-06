'''!
@file main.py
    This file is the top level running the machine that draws
    a picture using GCode. It utilizes drivers for low level
    components and 
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
    @brief Initalizes the encoders to their respective positons by first
    having the motors go all the way to the right and hitting the right
    limit switch, going all the way to the left and hitting the left limit
    switch, and then goes towards the center ceases all movement
    and waits for 1 second because it caused less initialize jitter
    All drivers have to be initliazed even though they are intialized again
    in cotask since this function is called before cotask
    """
    servo = servoDriver.ServoDriver(pyb.Pin.board.PA8, 1)
    servo.set_duty_cycle(5)
    switch1 = switchDriver.SwitchDriver(pyb.Pin.board.PC2)
    enc1 = encoderDriver.EncoderDriver(pyb.Pin.board.PB6,pyb.Pin.board.PB7, 4)
    switch2 = switchDriver.SwitchDriver(pyb.Pin.board.PC3)
    enc2 = encoderDriver.EncoderDriver(pyb.Pin.board.PC6,pyb.Pin.board.PC7, 8)
    moe1 = motorDriver.MotorDriver(pyb.Pin.board.PA10,
        pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    moe2 = motorDriver.MotorDriver(pyb.Pin.board.PC1,
        pyb.Pin.board.PA0, pyb.Pin.board.A1, 5)
    while switch1.getValue():
        #offset duty cycles reduced singularity issues
        moe1.set_duty_cycle(60)
        moe2.set_duty_cycle(40)
        enc1.update()
        enc2.update()
    enc1.zero()
    print("SWITCH 2 DONE!")
    while switch2.getValue():
        #offset duty cycles reduced singularity issues
        moe1.set_duty_cycle(-40)
        moe2.set_duty_cycle(-60)
        enc1.update()
        enc2.update()
    enc2.zero()
    print("SWITCH 1 DONE!")
    i = 0
    '''Cycle based stalling was the only way that I could get this to
    work as the motors would glitch out if I used utime.sleep or time.sleep()
    '''
    while i < 1000:
        #has it only for a few cycles so that it isn't hitting limit switch
        moe1.set_duty_cycle(40)
        moe2.set_duty_cycle(40)
        i = i + 1
        enc1.update()
        enc2.update()
    moe1.set_duty_cycle(0)
    moe2.set_duty_cycle(0)
    share_enc2.put(enc2.position)
    share_enc1.put(enc1.position)
    utime.sleep(1)
    


def task0_master ():
    """!
    Takes and converts GCode and passes to to program for drawing device
    It gets a list of tuples that we call "points" that have the format
    [x coordinate, y coordinate, z boolean]. We then convert the x and y coordinates
    to angles for the encoders. The z boolean is put into a share and used to tell the
    servo whether to be up or down
    """
    i = 0
    #filename has to be passed mannually
    points = gcode.get_instructions("balloon.nc")
    while True:
        for point in points:
             #print("X-Y: ",end="")
             #print(gcode.apply_(point)[0],gcode.apply_offset(point)[1])
             angles = kinematics.convertToEncoderAngles(gcode.apply_offset(point)[0],gcode.apply_offset(point)[1])
             #print(angles[0] * 180 / pi, angles[1] * 180 / pi)
             share_degree1.put(angles[0] * 180 / pi)
             share_degree2.put(angles[1] * 180 / pi)
             share_servo.put(point[2])
             yield(0)
        '''Decided to do a cycle stall loop since utime.sleep was not working
        50 is a completely arbitrary number but felt like enough time for it to wait
        for the servo to reset to high value so that it did not draw on the desk
        '''
        for i in range(0,50,1):
            share_servo.put(5)
            yield(0)

def task1_encoder1 ():
    """!
    This task creates a driver for one of the encoders being used.
    It puts the curent value of the encoder into a share to be used by other tasks
    There is a limit switch, and when pressed, it shows a unique message to the screen,
    zeros the encoder, stops the motor, puts zero into both encoder shares for this
    limit switch
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
    #phased out of final code
    moe = motorDriver.MotorDriver(pyb.Pin.board.PA10,
        pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    while True:
        moe.set_duty_cycle(share_motor1.get())
        yield(0)
        
def task3_control1 ():
    """!
    This task creates the controller that initilaizes the motors
    and a controller for each motor with a default arbitary value
    ( + or - 16092, but probably could have used a default of 45 degrees but was worried
    it would break code). The encoder value is then converted to an angle
    and is set as the new destination for the controller. The motor is set at
    the appropriate speed it should be at for reaching that destination
    Different gains work better for different images.
    Gain = 3000 for very curvy images.
    Gain = 5000 for more line heavy images.
    """
    moe1 = motorDriver.MotorDriver(pyb.Pin.board.PA10,
        pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    moe2 = motorDriver.MotorDriver(pyb.Pin.board.PC1,
        pyb.Pin.board.PA0, pyb.Pin.board.A1, 5)
    controller1 = controls.Controls(-16092, 3000/8192, 0)
    controller2 = controls.Controls(16092, 3000/8192, 0)
    while True:
        controller1.set_setpoint(-encoderDriver.degree_to_enc(share_degree1.get(), (7 / 2)))
        controller2.set_setpoint(encoderDriver.degree_to_enc(share_degree2.get(), (7 / 2)))
        moe2.set_duty_cycle(controller2.controlLoop(share_enc2.get()))
        moe1.set_duty_cycle(controller1.controlLoop(share_enc1.get()))
        yield(0)

'''
Phased out as having limit switch outside encoder was not logical
def task4_limitSwitch ():
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
    There is a limit switch, and when pressed, it shows a unique message to the screen,
    zeros the encoder, stops the motor, puts zero into both encoder shares for this
    limit switch
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
    #Phased out of final code
    moe = motorDriver.MotorDriver(pyb.Pin.board.PC1,
        pyb.Pin.board.PA0, pyb.Pin.board.A1, 5)
    while True:
        moe.set_duty_cycle(share_motor2.get())
        yield(0)
        
def task6_control2 ():
    #phased out of final code
    controller = controls.Controls(16092, 5000/8192, 0)
    while True:
        controller.set_setpoint(encoderDriver.degree_to_enc(share_degree2.get(), (7/2)))
        share_motor2.put(controller.controlLoop(share_enc2.get()))
        yield(0)
        
def task7_servo ():
    """!
    This task takes the value from the Servo share which is
    manipulated by the main GCode parser. 
    """
    #starts off at 5 degrees
    servo = servoDriver.ServoDriver(pyb.Pin.board.PA8, 1)
    while True:
        servo.set_duty_cycle(share_servo.get())
        yield(0)
    

"""! This main code first creates the shares that will be used to draw the picture
    and interpret the GCode,
     tasks and shares"""

if __name__ == "__main__":
    
    #Servo share is used for the servo PWM which is a percent
    #A PWM of 5 results in 45 degrees on the motor and PWM 1 is 0 degrees on motor
    share_servo = task_share.Share ('i', thread_protect = False, name = "Share Servo")

    #This is the shares that correlate the angle and encoder ticks
    #could be removed but added for troubleshooting and the readibility was too nice to remove
    share_degree1 = task_share.Share ('f', thread_protect = False, name = "Share Degree 1")
    share_degree2 = task_share.Share ('f', thread_protect = False, name = "Share Degree 2")
    
    #Shares for the encoder ticks that is used to communicate between encoder and controller
    share_enc1 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 1")
    share_enc2 = task_share.Share ('f', thread_protect = False, name = "Share Encoder 2")

    #
    share_motor1 = task_share.Share ('f', thread_protect = False, name = "Share Motor 1")
    share_motor2 = task_share.Share ('f', thread_protect = False, name = "Share Motor 2")
    
    
    
    #This task initlizes the encoders before cotask starts to run
    initialize_encoders()
    
    #for approx hourglass y offset = + 15 feed 5000, master period 25 enc period 10, motor 6, control 1
    #different drawings worker better with different refresh rates
    #task 2, 5, and 6 were merged into task 4 as it had better performance for non circle drawings
    task0 = cotask.Task (task0_master, name = 'Master', priority = 4, 
                         period = 120, profile = True, trace = False)
    task1 = cotask.Task (task1_encoder1, name = 'Encoder1', priority = 2, 
                         period = 5, profile = True, trace = False)
    task2 = cotask.Task (task2_motor1, name = 'Motor1', priority = 1, 
                         period = 3, profile = True, trace = False)
    task3 = cotask.Task (task3_control1, name = 'Controller1', priority = 1, 
                         period = 0.1, profile = True, trace = False)
    task4 = cotask.Task (task4_encoder2, name = 'Encoder2', priority = 2, 
                         period = 10, profile = True, trace = False)
    task5 = cotask.Task (task5_motor2, name = 'Motor2', priority = 1, 
                         period = 6, profile = True, trace = False)
    task6 = cotask.Task (task6_control2, name = 'Controller2', priority = 1, 
                         period = 1, profile = True, trace = False)
    task7 = cotask.Task (task7_servo, name = 'Servo', priority = 5, 
                         period = 20, profile = True, trace = False)
    
    cotask.task_list.append (task1)
    #cotask.task_list.append (task2)
    cotask.task_list.append (task4)
    #cotask.task_list.append (task5)

    
    '''
    #Original phased out initialization sequence
    initialized = False
    share_enc1.put(-8192)
    share_enc2.put(8192)
    while not initialized:
        cotask.task_list.pri_sched ()
        initialized = initialize_encoders()
        print("\n\n\n\nINITIALIZED\n\n\n")'''
    
    cotask.task_list.append (task0)
    cotask.task_list.append (task3)
    #cotask.task_list.append (task6)
    cotask.task_list.append (task7)

    #Active garbage collector for task share
    gc.collect ()

    #if any key is pressed, the task ends and prints data from task list
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

