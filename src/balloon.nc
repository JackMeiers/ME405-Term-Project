; Balloon test program.
G01 X3 Y3 F50 M5
G91 ; relative mode
G12 R1 F50 M4 ; draw circle for the balloon.
G03 X0 Y-1 I0 J-0.5 ; draw string.
G02 X0 Y-1 I0 J-0.5
G01 X-2 Y0 M5 ; Translate to draw ground.
G01 X4 Y0 M4 ; draw ground