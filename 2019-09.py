import numpy as np
import intcomputer as cmp

"""
--- Day 9: Sensor Boost ---
Int Computer v.9.0

Part 1:
The BOOST program will ask for a single input; run it in test mode by providing it the value 1. It will perform a series of checks on each opcode, output any opcodes (and the associated parameter modes) that seem to be functioning incorrectly, and finally output a BOOST keycode.

Once your Intcode computer is fully functional, the BOOST program should report no malfunctioning opcodes when run in test mode; it should only output a single value, the BOOST keycode. What BOOST keycode does it produce?

------------------------------------

Part 2:

The program runs in sensor boost mode by providing the input instruction the value 2. Once run, it will boost the sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor boost mode, the program will output a single value: the coordinates of the distress signal.

Run the BOOST program in sensor boost mode. What are the coordinates of the distress signal?

"""

#Test
progStr = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
prog = cmp.Program(progStr)
prog.run(debug=False)
out = prog.getOutputs()        
print("Output: " + str(out)) #copy of itself


#Part 1 ----------
prog = cmp.loadFromFile("puzzle09a.txt", inputs=[1])
prog.run(debug=False)
out = prog.getOutputs()        
print("Output: " + str(out)) #3601950151


#Part 2 ----------
prog = cmp.loadFromFile("puzzle09a.txt", inputs=[2])
prog.run(debug=False)
out = prog.getOutputs()        
print("Output: " + str(out)) #64236

