# -*- coding: utf-8 -*-
"""
--- Day 15: Oxygen System ---

Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated repair droid is your only option for fixing the oxygen system.

The Elves' care package included an Intcode program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

    Accept a movement command via an input instruction.
    Send the movement command to the repair droid.
    Wait for the repair droid to finish the movement operation.
    Report on the status of the repair droid via an output instruction.

Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.

What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?

Your puzzle answer was 280.

--- Part Two -------------------------------------------------------------------

You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes one minute for oxygen to spread to all open locations that are adjacent to a location that already contains oxygen. Diagonal locations are not adjacent.

Use the repair droid to get a complete map of the area. How many minutes will it take to fill with oxygen?
"""
import intcomputer as cmp
import numpy as np
import matplotlib.pyplot as plt


class Maze:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    MOVES = [(0, 0), (-1, 0), (+1, 0), (0, -1), (0, +1)]
    DIRECTIONS=['NONE', 'NORTH', 'SOUTH', 'WEST', 'EAST']

    ERROR = -1
    HIT_WALL = 0
    CMD_OK = 1
    TARGET_OK = 2
    RESULTS = ['HIT WALL', 'OK', 'TARGET']
    
    UNEXPLORED = 0
    WALL = 1
    EXPLORED = 2
    CURSOR = 2  
    FILLED = 5  
    
    def __init__(self, size=100):
        self.size = size
        self.grid = np.zeros((self.size,self.size), dtype=int)
        self.position = (int(self.size/2), int(self.size/2))
        self.grid[self.position] = self.CURSOR
        self.prog = cmp.loadFromFile("puzzle15.txt", [])
        
    def reset(self):
        self.position = (int(self.size/2), int(self.size/2))
        self.prog = cmp.loadFromFile("puzzle15.txt", [])
        
    def move(self, direction, write=False):
        self.prog.addInput(direction)
        self.prog.run()
        res = self.prog.getOutput(True)
        
        newPos = tuple(np.add(self.position, self.MOVES[direction]))
        
        if newPos[0]<0 or newPos[0]>=self.size-1 or newPos[1]<0 or newPos[1]>=self.size-1:
            print("Warn edge!")
            res=self.HIT_WALL
            self.grid[newPos] = self.WALL
        
        elif res==self.HIT_WALL:
            self.grid[newPos] = self.WALL

        elif res == self.CMD_OK or res == self.TARGET_OK:
            self.grid[self.position] = self.EXPLORED            
            self.grid[newPos] = self.CURSOR
            self.position = newPos

        if write:
            print("move " + self.DIRECTIONS[direction] + " - result: " + self.RESULTS[res] + " - position: " + str(self.position))
            
        return res

    def tryMove(self, direction):
        newPosition = tuple(np.add(self.position, self.MOVES[direction]))
        return self.grid[newPosition]
        
    
    def draw(self):
        #old = self.grid[self.position]
        #self.grid[self.position] = 2
        plt.imshow(self.grid)
        plt.show()
        #self.grid[self.position] = old
    
#------------------------------------------------------------------------------
        
        
nextMoveSequence = [[],[],[],[],[]]
nextMoveSequence[Maze.NORTH] = [Maze.EAST, Maze.NORTH, Maze.WEST, Maze.SOUTH]
nextMoveSequence[Maze.SOUTH] = [Maze.WEST, Maze.SOUTH, Maze.EAST, Maze.NORTH]
nextMoveSequence[Maze.WEST] = [Maze.NORTH, Maze.WEST, Maze.SOUTH, Maze.EAST]
nextMoveSequence[Maze.EAST] = [Maze.SOUTH,Maze.EAST, Maze.NORTH, Maze.WEST]

#Trova la mossa successiva più conveninente evitando i muri noti e privilegiando le regioni inesplorate
def findBestMove(maze, direction, write=False):
    dir = 0
    for i in range(0, 4):
        newDirection = nextMoveSequence[direction][i]
        res2 = maze.tryMove(newDirection)
        
        if res2==Maze.UNEXPLORED:
            if write:
                print("Best dir to unexplored: " + maze.DIRECTIONS[newDirection])
            return newDirection
        
        elif res2==Maze.WALL:
            continue
        
        elif res2==Maze.EXPLORED or res2==Maze.CURSOR:
            if dir==0: dir = newDirection

    if write:
        print("Best of nothing: " + maze.DIRECTIONS[dir])                        
    return dir


def explorePath(maze, write=False):
    maxSteps = 40000
    steps = 0    
    res = Maze.CMD_OK
    direction = Maze.NORTH 

    #Path contiene la lista delle caselle visitate
    #Se si reincontra una casella già visitata si eliminano le ultime caselle di path
    #in tal modo path contiene sempre il percorso minimo
    path = [maze.position]
    
    while res!=Maze.ERROR and steps<maxSteps:
        steps = steps + 1    
        
        direction = findBestMove(maze, direction, write)
        res = maze.move(direction, write)
        
        if maze.position in path:
            path = path[:path.index(maze.position)]            
    
        path.append(maze.position)
                
        if res==maze.TARGET_OK:
            print("Found: " + str(maze.position) + " after " + str(len(path)-1) + " steps (" + str(steps) + ")")  #(9,13) 280           
            return maze.position
        
    print("No result")
    return None
   
    
def fillFromPoint(maze, stack):
    stack0 = []
    
    while len(stack)>0:
        pos = stack.pop()
    
        for i in range(1, 5):
           newPos = tuple(np.add(pos, Maze.MOVES[i])) 
           if maze.grid[newPos] == Maze.EXPLORED:
               stack0.append(newPos)
               maze.grid[newPos] = Maze.FILLED
    return stack0
           
           
def fill(maze, startPoint):
    queue = []
    queue.append(startPoint)
    step = 0
    while len(queue)>0:
        
        if step%100==0:
            maze.draw()
            
        queue = fillFromPoint(maze, queue)
        step = step + 1
        
    print("2---->" + str(step-1))  #400
           
           
#------------------------------------------------------------------------------        

maze = Maze(50)
pos0 = (0,0)
for i in range(0, 4):
    pos = explorePath(maze)    
    if pos != None:
        pos0 = pos
    maze.reset()

maze.draw() 

print("Fill from point "+  str(pos0))

fill(maze, pos0)
maze.draw()    