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
    L1 = 9.8 
    edge_c = sqrt(x**2+y**2)
    #print("c: ", edge_c)
    edge_e = sqrt((D-x)**2 + y**2)
    #print("e: ",edge_e)
    delta = atan(y/x)
    #print("Delta :", delta)
    epsilon = acos((edge_e**2 - L2**2 + L1**2)/(2*L1*edge_c))
    #print("Epsilon :", epsilon)
    phi = acos((edge_c**2 - L2**2 + L1**2)/(2*L1*edge_c))
    #print("Phi :", phi)
    psi = atan(y/(D - x))
    #print("Psi :", psi)
    alpha = pi - (delta + phi) % pi
    beta = pi - (psi + epsilon) % pi
    #print("ALPHA,BETA: ", end='')
    #print(alpha,beta)
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
            radians = convertToEncoderAngles(3 + .625, 3 + 8)
            print(radians[0] * 180 / pi, radians[1] * 180 / pi)
    
    
    