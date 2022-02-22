'''!
@file gcode.py
Contains definitions for G code instruction object and basic translation functions.

@author Lucas Sandsor
@author Jack Barone
@author Jackson Meyers
@date 22-Feb-2022 
'''


"""
Short G-Code summary:
G00 - full-speed direct translation.
G01 - linear motion.
G02 - clockwise arc.
G03 - c-clockwise arc.
"""
class g_code_instruction:
    '''! Defines a basic structure for holding G code instructions.
    '''
    def __init__(self, line):
        '''! Creates a new instruction object based on a line of G code.
        @param line String containing a single line of G code.
        '''
        self.n = 0
        self.g = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.i = 0
        self.j = 0
        self.r = 0
        self.f = 0
        self.m = 0
        
        line = line.upper() # Make string uppercase.
        line = line.replace(';', ' ')
        blocks = line.split(' ')
        for i in range(len(blocks)):
            if blocks[i].startswith('N'): # Line number.
                self.n = int(blocks[i].replace('N', ''))
                continue
            if blocks[i].startswith('G'): # G code.
                self.g = int(blocks[i].replace('G', ''))
                continue
            if blocks[i].startswith('X'): # X coordinate.
                self.x = int(blocks[i].replace('X', ''))
                continue
            if blocks[i].startswith('Y'): # Y coordinate.
                self.y = int(blocks[i].replace('Y', ''))
                continue
            if blocks[i].startswith('Z'): # Z coordinate.
                self.z = int(blocks[i].replace('Z', ''))
                continue
            if blocks[i].startswith('I'): # X offset for arcs.
                self.i = int(blocks[i].replace('I', ''))
                continue
            if blocks[i].startswith('J'): # Y offset for arcs.
                self.j = int(blocks[i].replace('J', ''))
                continue
            if blocks[i].startswith('R'): # radius for arcs.
                self.r = int(blocks[i].replace('R', ''))
                continue
            if blocks[i].startswith('F'): # Feed rate instructions.
                self.f = int(blocks[i].replace('F', ''))
                continue
            if blocks[i].startswith('M'): # Use for enabling functions.
                self.m = int(blocks[i].replace('M', ''))
                continue

        # self.s # Spindle speed. Unused.
        # self.t # Tool commands. Shouldn't be necessary.


def get_instructions(filepath):
    '''! Opens a g code file and gets a list of all the instructions.
        @param filepath Path to .nc file.
    '''
    instructions = []
    print ("-I- Reading G code...")
    fh = open(filepath, 'r')
    
    lines = fh.readlines()
    # For each line in file:
    for line in lines:
        # Get instruction, add to list.
        instructions.append(g_code_instruction(line))
    
    print("-I- Reading G code... Done!")
    return instructions
    

if __name__ == "__main__":
    # Test translation
    instr = get_instructions("../sample2.nc")
    for ins in instr:
        print("\n\n")
        print("N: " + str(ins.n) + "\n")
        print("G: " + str(ins.g) + "\n")
        print("X: " + str(ins.x) + "\n")
        print("Y: " + str(ins.y) + "\n")
        print("Z: " + str(ins.z) + "\n")
        print("I: " + str(ins.i) + "\n")
        print("J: " + str(ins.j) + "\n")

