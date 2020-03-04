# -*- coding: utf-8 -*-
"""
--- Day 24: Planet of Discord ---


--- Part Two ---

After careful analysis, one thing is certain: you have no idea where all these bugs are coming from.

Then, you remember: Eris is an old Plutonian settlement! Clearly, the bugs are coming from recursively-folded space.

This 5x5 grid is only one level in an infinite number of recursion levels. The tile in the middle of the grid is actually another 5x5 grid, the grid in your scan is contained as the middle tile of a larger 5x5 grid, and so on. Two levels of grids look like this:

     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | |?| | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
     |     |-+-+-+-+-|     |     
     |     | | | | | |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
     |     |         |     |     
     |     |         |     |     

(To save space, some of the tiles are not drawn to scale.) Remember, this is only a small part of the infinitely recursive grid; there is a 5x5 grid that contains this diagram, and a 5x5 grid that contains that one, and so on. Also, the ? in the diagram contains another 5x5 grid, which itself contains another 5x5 grid, and so on.

The scan you took (your puzzle input) shows where the bugs are on a single level of this structure. The middle tile of your scan is empty to accommodate the recursive grids within it. Initially, no other levels contain bugs.

Tiles still count as adjacent if they are directly up, down, left, or right of a given tile. Some tiles have adjacent tiles at a recursion level above or below its own level. For example:

     |     |         |     |     
  1  |  2  |    3    |  4  |  5  
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
  6  |  7  |    8    |  9  |  10 
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |A|B|C|D|E|     |     
     |     |-+-+-+-+-|     |     
     |     |F|G|H|I|J|     |     
     |     |-+-+-+-+-|     |     
 11  | 12  |K|L|?|N|O|  14 |  15 
     |     |-+-+-+-+-|     |     
     |     |P|Q|R|S|T|     |     
     |     |-+-+-+-+-|     |     
     |     |U|V|W|X|Y|     |     
-----+-----+---------+-----+-----
     |     |         |     |     
 16  | 17  |    18   |  19 |  20 
     |     |         |     |     
-----+-----+---------+-----+-----
     |     |         |     |     
 21  | 22  |    23   |  24 |  25 
     |     |         |     |     

    Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
    Tile G has four adjacent tiles: B, F, H, and L.
    Tile D has four adjacent tiles: 8, C, E, and I.
    Tile E has four adjacent tiles: 8, D, 14, and J.
    Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
    Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.

The rules about bugs living and dying are the same as before.

For example, consider the same initial state as above:

....#
#..#.
#.?##
..#..
#....

The center tile is drawn as ? to indicate the next recursive grid. Call this level 0; the grid within this one is level 1, and the grid that contains this one is level -1. Then, after ten minutes, the grid at each level would look like this:

Depth -5:
..#..
.#.#.
..?.#
.#.#.
..#..

Depth -4:
...#.
...##
..?..
...##
...#.

Depth -3:
#.#..
.#...
..?..
.#...
#.#..

Depth -2:
.#.##
....#
..?.#
...##
.###.

Depth -1:
#..##
...##
..?..
...#.
.####

Depth 0:
.#...
.#.##
.#?..
.....
.....

Depth 1:
.##..
#..##
..?.#
##.##
#####

Depth 2:
###..
##.#.
#.?..
.#.##
#.#..

Depth 3:
..###
.....
#.?..
#....
#...#

Depth 4:
.###.
#..#.
#.?..
##.#.
.....

Depth 5:
####.
#..#.
#.?#.
####.
.....

In this example, after 10 minutes, a total of 99 bugs are present.

Starting with your scan, how many bugs are present after 200 minutes?

Your puzzle answer was 2047.
"""

import numpy as np
import math

class BugWorld:
    
    UP = (-1, 0)
    DOWN = (+1, 0)
    LEFT = (0, -1)
    RIGHT = (0, +1)
    MOVES = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, fileName):
        with open(fileName, "r") as f:
            rows = f.readlines()
            grid = [ [str(c) for c in str(row) if c!='\n' ] for row in rows ]
        grid = np.array(grid)

        self.shape = (-1 ,-1)
        self.center = (-1 ,-1)

        grid = self.decoreGrid(grid)

        self.levels = list()
        self.levels.append(grid)
   
    
    def decoreGrid(self, grid):
        dx = grid.shape[1]
        grid = np.append([["." for i in range(0, dx)]], grid, axis=0)            
        grid = np.append(grid, [["." for i in range(0, dx)]], axis=0)            
        

        dy = grid.shape[0]              
        col = np.array(["." for i in range(0, dy)])        
        grid = np.append( grid, col[:,None], axis=1)

        col = np.array(["." for i in range(0, dy)])        
        grid = np.append(col[:,None], grid, axis=1)

        self.shape = grid.shape
        self.center = (math.floor(self.shape[0]/2), math.floor(self.shape[0]/2))
        grid[self.center] = "?"
        return grid
        
    
    def addUpperLevelElements(self, l):
        if l==0:
            return
        
        el = self.levels[l-1][tuple(np.add(self.center, BugWorld.UP))] 
        for i in range(0, self.shape[1]):
            self.levels[l][(0, i)] = el 

        el = self.levels[l-1][tuple(np.add(self.center, BugWorld.DOWN))]            
        for i in range(0, self.shape[1]):
            self.levels[l][(self.shape[0]-1, i)] = el 

        el = self.levels[l-1][tuple(np.add(self.center, BugWorld.LEFT))]            
        for i in range(0, self.shape[1]):
            self.levels[l][(i, 0)] = el 

        el = self.levels[l-1][tuple(np.add(self.center, BugWorld.RIGHT))]            
        for i in range(0, self.shape[1]):
            self.levels[l][(i, self.shape[1]-1)] = el 

        
    def getLowerLevelElementCount(self, l, d):
        if len(self.levels)==l+1:
            return 0
        
        c = 0        
        if d == BugWorld.RIGHT:
            for i in range(1, self.shape[0]-1):
                newPos = (i, 1)
                if self.levels[l+1][newPos] == "#":
                    c = c + 1
        elif d == BugWorld.LEFT:
            for i in range(1, self.shape[0]-1):
                newPos = (i, self.shape[1]-2)
                if self.levels[l+1][newPos] == "#":
                    c = c + 1
        elif d == BugWorld.UP:
            for i in range(1, self.shape[1]-1):
                newPos = (self.shape[0]-2, i)
                if self.levels[l+1][newPos] == "#":
                    c = c + 1
        elif d == BugWorld.DOWN:
            for i in range(1, self.shape[1]-1):
                newPos = (1, i)
                if self.levels[l+1][newPos] == "#":
                    c = c + 1
        return c
    
    
    def getEmptyGrid(self):
        newgrid = np.array([["." for i in range(1, self.shape[1]-1)] for i in range(1, self.shape[0]-1)])
        newgrid = self.decoreGrid(newgrid) 
        return newgrid
            
    
    def evolveOneLevel(self, mygrid, l):        
        for y in range(1, len(mygrid)-1):
            row = mygrid[y]
            for x in range(1, len(row)-1):
                c = 0
                pos = (y, x)
                el0 = self.levels[l][pos]
                
                if el0 == "?":
                    continue
                
                for i in range(0, 4):
                    el = self.levels[l][tuple(np.add(pos, BugWorld.MOVES[i]))]
                    
                    if el=='#':
                        c += 1
                    
                    #Elemento centrale: devo considerare l'elemento del livello inferiore
                    elif el=="?":
                        c += self.getLowerLevelElementCount(l, BugWorld.MOVES[i]) 
                        
                if el0 == '#' and c==1:
                    mygrid[pos] = '#'
                elif el0 == '.' and (c==1 or c==2):
                    mygrid[pos] = '#'
                else:
                    mygrid[pos] = '.'                    


    def evolveOneStep(self):
        self.levels.insert(0, self.getEmptyGrid())
        self.levels.append(self.getEmptyGrid())

        mylevels = self.levels.copy()                
        for l in range(0, len(mylevels)):
            grid = mylevels[l].copy()
            self.addUpperLevelElements(l)
            self.evolveOneLevel(grid, l)                        
            mylevels[l] = grid
            
        self.levels = mylevels.copy()
    
    
    def getBugCount(self):
        c = 0
        for lev in self.levels:
            c += np.sum(lev=="#")
        return c


    def printMap(self):
        i = 0
        for mygrid in self.levels:
            print("level: ", i,"------")                            
            i +=1
            for row in mygrid[1:-1]:
                s = ''.join([c for c in row[1:-1]])
                print(s)


#Part 1-----------------------------------------------------------------------

bs = set()
myworld = BugWorld("puzzle24.txt")

for i in range(0, 200):
    myworld.evolveOneStep()
    
#myworld.printMap()

print("2---->", myworld.getBugCount())