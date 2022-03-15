'''!@file                mainpage.py
   @brief               Page describing work for final project in ME405
   @details             Desribes the details of the arm pen plotter used
                        to draw an given image
                        
   @mainpage
                        
   @section wel         Howdy!
                        This website serves as documentation of all labs 
                        and projects done during the Winter of 2022 in ME 405 -
                        Mechatronics. If you have any questions, please contact: 
                        baronejohn00@gmail.com or
                        lukesandsor@aol.com or
                        jpmeyers@calpoly.edu
                        
                        The majority of assignments are drivers on controlling
                        a motors to control a pen plotter that takes G code and
                        uses a sharpie to draw that picture.
                                                
   @section source      Source Code
                        All source code for this project is available here:
                        https://github.com/JackMeiers/ME405-Term-Project
                        

   @subsection Task Diagram    Overview
                        This is the overhead of the main task diagram that will run our
                        program. 
                        
                        \image html TaskDiagram.png
                        
                        This is the high level task diagram used to run our program
                        
   @subsection State Diagram   General Prototype FSM
                        This is the prototype FSM used to outline the general way that we wanted out
                        code to run. It was how we structured the task diagram and is the
                        basis for our entire program. Though not followed exactly it outlines
                        key steps in making our machine work
                        
                        \image html GcodeConverterFSM.png
                        
   @subsection State2 Diagram   Initialization Sequence
                        This the initialization sequence that the program does as soon as it boots.
                        This ensures the the encoder values are properly zeroed and that the arms start
                        in a somewhat centered position. It also guarantees that the pen is raised while
                        initializing so that we do not draw on a surface outside our intended canvas
                        
                        \image html InitializeFSM.png
    
   @subsection Component Drivers
                        For each of the components on the machine we have a driver alongside a
                        non-component driver in the shape of a motor controller built using software.
                        Each of these drivers is used in the higher level functions
            
   @subsection GCode Parser
                        We needed a way to analyze and interact with a GCode file when it is passed
                        to the board. The"gcode.py" module is used for this and passes the parsed
                        GCode in the format of [x,y,z] using a tuple. The file name must be edited
                        in "main.py" and loaded on the board
    
                        
   @author              Jack Barone
   @author              Jack Meyers
   @author              Luke Sandsor
   
   @date                February 25th, 2022
'''