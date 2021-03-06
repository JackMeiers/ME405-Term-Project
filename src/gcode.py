'''!@file gcode.py
@brief Contains definitions for G code instruction object and basic translation functions.

@author Lucas Sandsor
@author Jack Barone
@author Jackson Meyers
@date 22-Feb-2022 
'''

#import task_share
import math as m

# conversion to have each step run in .1s.
FEED_CONVERSION = 0.001666

class g_code_instruction:
    '''! @brief Defines a basic structure for holding G code instructions.
    '''
    def __init__(self, line):
        '''! @brief Creates a new instruction object based on a line of G code.
        @param line String containing a single line of G code.
        '''
        self.n = 0
        self.g = -1
        self.x = 0
        self.y = 0
        self.z = 0
        self.i = 0
        self.j = 0
        self.r = 0
        self.f = 0
        self.m = 0
        
        line = line.upper() # Make string uppercase.
        #line = line.replace(';', ' ')
        blocks = line.split(' ')
        for i in range(len(blocks)):
            if blocks[i].startswith(';'):
                break
            if blocks[i].startswith('N'): # Line number.
                self.n = int(blocks[i].replace('N', ''))
                continue
            if blocks[i].startswith('G'): # G code.
                self.g = int(blocks[i].replace('G', ''))
                continue
            if blocks[i].startswith('X'): # X coordinate.
                self.x = float(blocks[i].replace('X', ''))
                continue
            if blocks[i].startswith('Y'): # Y coordinate.
                self.y = float(blocks[i].replace('Y', ''))
                continue
            if blocks[i].startswith('I'): # X offset for arcs.
                self.i = float(blocks[i].replace('I', ''))
                continue
            if blocks[i].startswith('J'): # Y offset for arcs.
                self.j = float(blocks[i].replace('J', ''))
                continue
            if blocks[i].startswith('R'): # radius for arcs.
                self.r = float(blocks[i].replace('R', ''))
                continue
            if blocks[i].startswith('F'): # Feed rate instructions.
                self.f = int(blocks[i].replace('F', ''))
                continue
            if blocks[i].startswith('M'): # Use for enabling functions.
                self.m = int(blocks[i].replace('M', ''))
                continue
            if blocks[i].startswith('P'): # Timing.
                self.p = float(blocks[i].replace('P', ''))
                continue
        # self.s # Spindle speed. Unused.
        # self.t # Tool commands. Shouldn't be necessary.
        
    def isRepeat(self):
        '''! @brief Returns whether the instruction is a repeat of previous instruction.
        '''
        return self.g == -1 and (self.x != 0 or self.y != 0 or self.i != 0 or self.j != 0 or self.r != 0)


class g_code_settings:
    '''! @brief Holds settings between function runs.
    '''
    def __init__(self):
        self.feed_rate = 60
        self.absolute = 0
        self.last_g = -1
        self.pen = 5

def get_instructions(filepath):
    '''! @brief Opens a g code file and gets a list of all the instructions.
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
    
    positions = []
    settings = g_code_settings()
    positions += [(0,0,0)]
    for instr in instructions:
        test = execute(instr, positions[-1], settings)
        positions += test
    
    print("-I- Reading G code... Done!")
    #for i in range(0,len(positions)-1):
    #    positions[i] = apply_offset(positions[i][0], positions[i][1])
    return positions

def execute(instruction, position, settings):
    '''! @brief Generates the points for a given instruction.
    @param instruction The instruction to be run.
    @param position The current position of the pen.
    @param settings g_code_settings object with this program's current settings.
    '''
    # G codes.
    # Operations.
    if (instruction.f != 0):
        settings.feed_rate = instruction.f
    
    # M codes.
    if (instruction.m == 30): # signal program end w/ reset.
        # put settings back to default and zero.
        return [(0,0,0)]
    
    elif (instruction.m == 3 or instruction.m == 4): # put pen down.
        settings.pen = 1

    elif (instruction.m == 5): # pull pen up.
        settings.pen = 5

    elif (instruction.m == 47): # repeat from first line.
        return [(0,0, settings.pen)]
    
    if (instruction.isRepeat()): # repeat last instruction w/ new x,y,i,j
        if (settings.last_g==-1):
            print("Error: bad g code formatting")
        instruction.g = settings.last_g
        
    if (instruction.g == 0 or instruction.g == 1): # full speed translation.
        # Convert from relative to absolute if necessary.
        settings.last_g = instruction.g
        if (settings.absolute == 0):
            abs_point = abs_to_rel(position, instruction.x, instruction.y)
            instruction.x = abs_point[0]
            instruction.y = abs_point[1]
        
        if (instruction.g == 1): # interpolated linear movement.
            return linear(position, instruction.x, instruction.y, settings.pen, settings.feed_rate)
        return linear(position, instruction.x, instruction.y, settings.pen)

    elif (instruction.g == 2 or instruction.g == 3): # cw or ccw arc.
        settings.last_g == instruction.g
        direction = instruction.g % 2
        # Convert from relative to absolute if necessary.
        if (settings.absolute == 0):
            abs_point = abs_to_rel(position, instruction.x, instruction.y)
            instruction.x = abs_point[0]
            instruction.y = abs_point[1]
        
        if (instruction.r!=0):
            return arcr(position, direction, instruction.r, settings.pen, settings.feed_rate, instruction.x, instruction.y)

        return arc(position, direction, instruction.i, instruction.j, settings.pen, settings.feed_rate, instruction.x, instruction.y)

    elif (instruction.g == 12 or instruction.g == 13): # cw or ccw circle.
        settings.last_g = instruction.g
        direction = instruction.g % 12
        if (instruction.r!=0):
            return arcr(position, direction, instruction.r, settings.pen, settings.feed_rate)
        
        return arc(position, direction, instruction.i, instruction.j, settings.pen, settings.feed_rate)
          
    elif (instruction.g == 28): # zero return.
        return [(0,0,0)]
    elif (instruction.g == 9): # exact stop.
        return [position,position,position,position,position]    

    elif (instruction.g == 4): # dwell.
        waitpoints = []
        for o in range(instruction.p * 10):
            points.append(position)
        return waitpoints
    # Change settings.
    if (instruction.g == 90 or instruction.g == 91):
        # G90 = absolute positioning, G91 is relative positioning.
        settings.absolute = instruction.g % 90
    
    return []
        

def distance(start, end):
    '''! @brief Calculates the distance between two points
        @param start 2D or 3D point at the starting position.
        @param end 2D or 3D point at the ending position.
    '''
    delta_x = end[0] - start[0]
    delta_y = end[1] - start[1]

    return m.sqrt(pow(delta_x,2) + pow(delta_y,2))

def linear(pos, x_rel, y_rel, pen, feed=-1):
    '''! @brief Generates the set of points for drawing a line.
        @param pos The position of the pen at the beginning of the line.
        @param x_rel The X coordinate of the line's end point.
        @param y_rel The Y coordinate of the line'e end point.
        @param pen The duty cycle of the pen servo for this operation.
        @param feed The feed rate of the operation. If feed is -1, will perform a full-speed move
    '''
    start_point = pos
    end_point = (pos[0] + x_rel, pos[1] + y_rel, pen)
    points = [end_point]
    
    distance1 = distance(start_point, end_point)
    
    if (feed != -1):
        step = feed * FEED_CONVERSION
    else:
        return points
    
    u = ((end_point[0] - start_point[0])/distance1, (end_point[1] - start_point[1])/distance1)
    
    d = step
    while d < distance1:
        new_point = (start_point[0] + u[0] * d, start_point[1] + u[1] * d, pen)
        points.insert(-1,new_point)

        d += step
    
    return points

def arc(pos, direction, i, j, pen, feed, x_rel=0, y_rel=0):
    '''! @brief Generates and returns the set of points to draw an arc.
        @param pos The starting position of the arc.
        @param direction The direction of the arc, 0 for clockwise, 1 for counter-clockwise.
        @param i The x position of the center of the arc.
        @param j The y position of the center of the arc.
        @param pen The state of the pen. 1 for pen down, 5 for pen up.
        @param feed The feed rate of the operation. Given in inches per minute.
        @param x_rel The x coordinate of the arc's end point.
        @param y_rel The y coordinate of the arc's end point.
    '''
    start_point = pos
    end_point = (pos[0] + x_rel, pos[1] + y_rel, pen)
    center_point = (pos[0] + i,pos[1] + j)
    if (direction == 0): # map directions
        direction = -1
    
    step = feed * FEED_CONVERSION
    radius = distance(start_point, center_point)
    
    points = [end_point]

    # offset from 0 radians to starting point
    if (i == 0):
        i = 0.0000001
    offset = m.pi + m.atan(j/i)
    
    # If start and end points are the same, draw a full circle.
    if (x_rel == 0 and y_rel == 0):
        angle = 2 * m.pi
    else:
        i_comp = i * (i - x_rel)
        j_comp = j * (j - y_rel)
        val = (i_comp + j_comp)
        if (val > 1):
            val = val % 2 - 1
        angle = m.acos(val/m.pow(radius,2))
        if (direction == 1):
            angle = 2 * m.pi - angle
    
    # calculate total length to travel.
    arc_length = radius * angle
    d = step
    while d < arc_length:
        theta = direction * d / radius
        x = radius * m.cos(theta + offset) + center_point[0]
        y = radius * m.sin(theta + offset) + center_point[1]
        points.insert(-1, (x, y, pen))
        d += step
          
    return points

def find_j(r,x,y):
    '''! @brief Calculates the y coordinate of the center of an arc based on the radius and end point.
    @param r The radius in inches.
    @param x The x coordinate of the end point.
    @param y The y coordinate of the end point.
    
    @return 
    '''
    scale = 1
    if (r < 0):
        scale = -1
    r = abs(r)
    root = 4 * r**2 * x**4 + 4 * r**2 * x**2 * y**2 - x**6 - 2 * x**4 * y**2 - x**2 * y**4
    num = scale * m.sqrt(root) + x**2 * y + y**3
    denom = 2 * (x**2 + y**2)
    
    return num/denom

def find_i(r,j):
    '''! @brief Calculates the x coordinate of the center of the arc, based on the radius and the center's y coordinate.
        @param r The radius of the circle in inches.
        @param j The y coordinate of the center point, calculated using find_j().
    '''
    return m.sqrt(r**2 - j**2)

    
def arcr(pos, direction, r, pen, feed, x_rel=0, y_rel=0):
    '''! @brief Generates and returns the set of points to draw an arc.
        @param pos The starting position of the arc.
        @param direction The direction of the arc, 0 for clockwise, 1 for counter-clockwise.
        @param r The radius of the circle. A negative value will draw the short arc for the given value, while a positive value will draw the long arc.
        @param pen The state of the pen. 1 for pen down, 5 for pen up.
        @param feed The feed rate of the operation. Given in inches per minute.
        @param x_rel The x coordinate of the arc's end point.
        @param y_rel The y coordinate of the arc's end point.
    '''
    start_point = pos
    end_point = (pos[0] + x_rel, pos[1] + y_rel, pen)
    if (direction == 0): # map directions
        direction = -1
        
    step = feed * FEED_CONVERSION
    points = [end_point]
    if(x_rel != 0 or y_rel != 0):
        j = find_j(r, x_rel, y_rel)
        i = find_i(r, j)
    else:
        j = r
        i = 0
    #print("i: " + str(i) + ", j: " + str(j))
    center_point = (pos[0] + i, pos[1] + j)
    if i == 0:
        i = 0.00000000001
    offset = m.pi + m.atan(j/i)
    if (r < 0):
        # Choose long arc
        r = abs(r)
    
    if (x_rel == 0 and y_rel == 0):
        angle = 2 * m.pi
    else:
        #print(str(i) + " " + str(j))
        val = (i * (i - x_rel)+ j * (j - y_rel))
        #print(val)
        if (val > 1):
            val = (val % 2) - 1
        angle = m.acos(val/m.pow(r,2))
        if (direction == 1):
            angle = 2 * m.pi - angle
    
    # calculate total length to travel.
    arc_length = r * angle
    d = step
    while d < arc_length:
        theta = direction * d / r
        x = r * m.cos(theta + offset) + center_point[0]
        y = r * m.sin(theta + offset) + center_point[1]
        points.insert(-1, (x,y, pen))
        d += step
          
    return points
    
def abs_to_rel(current_pos, x, y):
    '''! @brief Converts a point in absolute space, to a point relative to the passed position.
        @param current_pos The position that serves as the origin of the relative point.
        @param x The absolute x value of the point to be converted.
        @param y The absolute y value of the point to be converted.
    '''
    return (x - current_pos[0], y - current_pos[1])

def rel_to_abs(current_pos, x, y):
    '''! @brief Converts a point in relative space to absolute space.
        @param current_pos Position that serves as the origin of the relative point.
        @param x The relative x value of the point to be converted.
        @param y The relative y value of the point to be converted.
    '''
    return (current_pos[0] + x, current_pos[1] + y)

def apply_offset(point):
    '''! @brief Applies an offset to convert from absolute space to the robot's drawing space.
        @param point The point to apply the offset to.
    '''
    return (point[0] - 2, point[1] + 15)

if __name__ == "__main__":
    # debug code
    # points = linear((2,2), 1, 3, 60)
    # points = arcr((2,2),0, 1.4, 60, 2, 0)
    points = get_instructions("../flower.nc")
    for i in points:
        print("(" + str(i[0]) + "," + str(i[1]) + ")\n")
