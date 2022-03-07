'''!
@file kinematics
This file contains information for the kinematics of the 
system and how we got the values for the arm movement
@author Lucas Sandsor
@author Jack Barone
@author Jackson Myers
@date 26-Feb-2022 
'''
from math import acos
from math import atan
from math import cos
from math import sin
from math import pi
from math import sqrt


def convertToEncoderAngles(x, y):
    """!based off the kinematic equations created in kinematics.PNG
        @retuns Tuple containing the angle for the first encoder and
        the angle for the second encoder
    """
    #Does this so that there is no divde by zero error
    #Approximation to 1 microinch causes nearly no change in angles
    if x == 0:
        x = 0.00001
    if y == 0:
        y = 0.00001
    D = 1.25
    L2 = 10
    L1 = 10.2
    ## Need to measure L3 and Pangle. I guessed, problaly close
    # L3 should be distance from pen center to bearing center in joint
    # Pangle should be the line L3 makes with the carbon fibe tube.
    L3 = 1
    pangle = 120 * (pi/180)
    
    edge_c = sqrt(x**2+y**2)
    #print("c: ", edge_c)
    edge_e = sqrt((D-x)**2 + y**2)
    #print("e: ",edge_e)
    delta = atan(y/x)
    #print("Delta :", delta)
    epsilon = acos((edge_e**2 - L2**2 + L1**2)/(2*L1*edge_e))  #used wrong edge here!, changed it already
    #print("Epsilon :", epsilon)
    # r
    phi = acos((edge_c**2 - L2**2 + L1**2)/(2*L1*edge_c))
    #print("Phi :", phi)
    psi = atan(y/(D - x))
    #print("Psi :", psi)
    alpha = pi - (delta + phi) % pi
    beta = pi - (psi + epsilon) % pi
    #print("ALPHA,BETA: ", end='')
    #kinprint(alpha,beta)
    ## Now calculate for pen offset
    C = acos((L2**2 + L1**2 - edge_e**2)/(2*L1*L2))
    J = pi - (C-beta)
    x = x - L3 * cos(J - (pi - pangle))
    y = y - L3 * sin(J - (pi - pangle))
    ## recalc with new x y positions
    edge_c = sqrt(x**2+y**2)
    #print("c: ", edge_c)
    edge_e = sqrt((D-x)**2 + y**2)
    #print("e: ",edge_e)
    delta = atan(y/x)
    #print("Delta :", delta)
    epsilon = acos((edge_e**2 - L2**2 + L1**2)/(2*L1*edge_e))  #used wrong edge here!, changed it already
    #print("Epsilon :", epsilon)
    # r
    phi = acos((edge_c**2 - L2**2 + L1**2)/(2*L1*edge_c))
    #print("Phi :", phi)
    psi = atan(y/(D - x))
    #print("Psi :", psi)
    alpha = pi - (delta + phi) % pi
    beta = pi - (psi + epsilon) % pi
    
    return (alpha, beta)
    
    
def arccos(radians):
    """!created a new arccos using math.acos with improvements
    for usage"
    """
    if radians <= 0:
        radians = (radians % -pi)
    else:
        radians = (radians % pi)
    if radians >= 1:
        return pi
    elif radians <= -1:
        return -(pi)
    else:
        return acos(radians)
    

if __name__ == "__main__":
            radians = convertToEncoderAngles(-2, 10)
            print(radians[0] * 180 / pi, radians[1] * 180 / pi)
    
    
    