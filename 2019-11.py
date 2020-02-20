import intcomputer as cmp
import numpy as np
import matplotlib.pyplot as plt
import operator

"""
--- Day 11: Space Police ---

Part 1:
You'll need to build a new emergency hull painting robot. The robot needs to be able to move around on the grid of square panels on the side of your ship, detect the color of its current panel, and paint its current panel black or white. (All of the panels are currently black.)

The Intcode program will serve as the brain of the robot. The program uses input instructions to access the robot's camera: provide 0 if the robot is over a black panel or 1 if the robot is over a white panel. Then, the program will output two values:

    First, it will output a value indicating the color to paint the panel the robot is over: 0 means to paint the panel black, and 1 means to paint the panel white.
    Second, it will output a value indicating the direction the robot should turn: 0 means it should turn left 90 degrees, and 1 means it should turn right 90 degrees.

After the robot turns, it should always move forward exactly one panel. The robot starts facing up.

---------------------------------------------

Part 2:
You're not sure what it's trying to paint, but it's definitely not a registration identifier. The Space Police are getting impatient.

Checking your external ship cameras again, you notice a white panel marked "emergency hull painting robot starting panel". The rest of the panels are still black, but it looks like the robot was expecting to start on a white panel, not a black one.

Based on the Space Law Space Brochure that the Space Police attached to one of your windows, a valid registration identifier is always eight capital letters. After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?
"""

class HullPauntungRobot:
        
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    TURN_LEFT = 0
    TURN_RIGHT = 1
        
    def __init__(self, grid, pos, prog):
        self.grid = grid
        self.paintedCells = np.zeros(grid.shape)
        self.pos = pos
        self.prog = prog
        self.pointTo = self.UP

    def run(self):
        
        while(not self.prog.ended):
            self.prog.addInput(self.grid[self.pos])
            self.prog.run()
            col = self.prog.getOutput()
            cmd = self.prog.getOutput()
            
            self.grid[self.pos] = col
            self.paintedCells [self.pos] = 1
            
            if cmd==self.TURN_LEFT:
                self.pointTo = (self.pointTo - 1)%4
                #print("Paint "+  str(col) + " - turn left")
            elif cmd==self.TURN_RIGHT:
                self.pointTo = (self.pointTo + 1)%4
                #print("Paint "+  str(col) + " - turn right")
                
            if   self.pointTo==self.UP:
                self.pos = tuple(map(operator.add, self.pos, (-1, 0)))
            elif self.pointTo==self.RIGHT:
                self.pos = tuple(map(operator.add, self.pos, (0, +1)))
            elif self.pointTo==self.DOWN:
                self.pos = tuple(map(operator.add, self.pos, (+1, 0)))
            elif self.pointTo==self.LEFT:
                self.pos = tuple(map(operator.add, self.pos, (0, -1)))
            

    def paint(self):
        plt.imshow(self.grid)
        plt.show()
     
    def getPaintedCellsNumber(self):
        return len(self.paintedCells[self.paintedCells==1])




#Part 1------------------------------------------------------------------------    
"""
size = 100
grid = np.zeros((2*size+1, 2*size+1), dtype=int)
startPos = (size, size)

prog = cmp.loadFromFile("puzzle11.txt")

robot = HullPauntungRobot(grid, startPos, prog)
robot.run()
robot.paint()

print(robot.getPaintedCellsNumber())  #2415
"""

#Part 2------------------------------------------------------------------------
size = 100
grid = np.zeros((2*size+1, 2*size+1), dtype=int)
startPos = (size, size)
grid[startPos] = 1

prog = cmp.loadFromFile("puzzle11.txt")

robot = HullPauntungRobot(grid, startPos, prog)
robot.run()
robot.paint() #BFPUZUPC

print(robot.getPaintedCellsNumber())