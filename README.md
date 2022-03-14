# ME405 Term Project

### Introduction
This goal of this project was to create a plotting robot capable of drawing images onto paper. The project allowed us to implement motion control, multitasking, and proper program orginization. The plotter must consist of 2.5 axis. The first two axis must 

### Description
Our design uses a dual-arm plotter design. 
There will be two rotating arms connected to our positioning motors and two non-actuated joints that link to the carriage that holds the pen. 
By controlling the angles of the rotating arms, the plotter will control the pen position.
We will contain our positioning motors in a 3D-printed base and use a cam under the base to slightly lift and drop the pen.

G code will be used to communicate the pen position and movement to the plotter. We plan to use some light carbon fiber rods for our linkages. Our nucleo can provide the operating voltage for the servo,
so we will use either the bench power supply or a 12V battery to provide power to the motors.

### Bill Of Materials
| Qty. | Part                  | Source                | Est. Cost |
|:----:|:----------------------|:----------------------|:---------:|
|  2   | Pittman Gearmotors    | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe      | ME405 Tub             |     -     |
|  1   | Lime Green Sharpie    | Staples               |   $1.02   |
|  1   | Hobby Servo           | Personal              |     -     |
|  2   | Carbon Fiber rods     | McMaster-Carr         |    $15    |
|  6   | 1/4" Bearing          | Amazon                |    $20    |
|  2   | 1/4" Steel Shaft      | McMaster-Carr         |    $16    |
|  1   | H bridge Motor Driver | Personal              |     -     | 

### Sketch
![Sketch go here](./sketch.PNG)

### Referenced Diagram
![Diagram go here](./diagram.png)
We based our design off of this previously done project, source is below:
https://portfolium.com/entry/pen-gripping-dual-scara-arm-plotter

### Hardware 
After iterating on the plotter design, we came up with a final design shown below. 

![FullCAD go here](./fullcad.PNG)
![cadofgears go here](./cadofgears.PNG)

The majority of our components were 3D printed. We 3D printed hubs with gear teeth to mesh with the puttman gear motors. That gear ratio was a 2/7 slowdown. This allowed us to have a higher resolution. The main housing was held together using threaded thermal inserts and M3 bolts. The use of carbon fiber decreased the inertia of our system and allowed us to move quickly. In the CAD, we included a tilt axis at the base of our main housing. We decided to scrap this and instead move the servo to the end of the linkage next to the pen. Also, we decided to offset the pen so that it didn't act through the bearings. Epoxy was added at the joints to strengthen. Changes showed below. 

![changes](./changes.PNG)


### Video Links 
1 - https://youtu.be/_5m5r6dnIIY 
2 - https://youtu.be/3c9mipRUHZs 
3 - https://youtu.be/eMAQph7v7VM 


