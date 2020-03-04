# -*- coding: utf-8 -*-
"""
--- Day 24: Planet of Discord ---

You land on Eris, your last stop before reaching Santa. As soon as you do, your sensors start picking up strange life forms moving around: Eris is infested with bugs! With an over 24-hour roundtrip for messages between you and Earth, you'll have to deal with this problem on your own.

Eris isn't a very large place; a scan of the entire area fits into a 5x5 grid (your puzzle input). The scan shows bugs (#) and empty spaces (.).

Each minute, The bugs live and die based on the number of bugs in the four adjacent tiles:

    A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
    An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.

Otherwise, a bug or empty space remains the same. (Tiles on the edges of the grid have fewer than four adjacent tiles; the missing tiles count as empty space.) This process happens in every location simultaneously; that is, within the same minute, the number of adjacent bugs is counted for every tile first, and then the tiles are updated.

Here are the first few minutes of an example scenario:

Initial state:
....#
#..#.
#..##
..#..
#....

After 1 minute:
#..#.
####.
###.#
##.##
.##..

After 2 minutes:
#####
....#
....#
...#.
#.###

After 3 minutes:
#....
####.
...##
#.##.
.##.#

After 4 minutes:
####.
....#
##..#
.....
##...

To understand the nature of the bugs, watch for the first time a layout of bugs and empty spaces matches any previous layout. In the example above, the first layout to appear twice is:

.....
.....
.....
#....
.#...

To calculate the biodiversity rating for this layout, consider each tile left-to-right in the top row, then left-to-right in the second row, and so on. Each of these tiles is worth biodiversity points equal to increasing powers of two: 1, 2, 4, 8, 16, 32, and so on. Add up the biodiversity points for tiles with bugs; in this example, the 16th tile (32768 points) and 22nd tile (2097152 points) have bugs, a total biodiversity rating of 2129920.

What is the biodiversity rating for the first layout that appears twice?

Your puzzle answer was 27777901.
"""

import numpy as np

class BugWorld:
    
    MOVES = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

    @staticmethod
    def __printMap(m):
        s = ''
        for row in m:
            s = ''.join([c for c in row])
            print(s) 
            
            
    def __init__(self, fileName):
        with open(fileName, "r") as f:
            self.rows = f.readlines()
            self.grid = [ [str(c) for c in str(row) if c!='\n' ] for row in self.rows ]
            for row in self.grid:
                row.insert(0, ".")
                row.append(".")
            self.grid.insert(0, ["." for x in self.grid[0]])
            self.grid.append(["." for x in self.grid[0]])
            self.grid = np.array(self.grid)
    
        
    def evolveOneStep(self):
        mygrid = self.grid.copy()
        for y in range(1, len(mygrid)-1):
            row = mygrid[y]
            for x in range(1, len(row)-1):
                c = 0
                pos = (y, x)
                for i in range(0, 4):
                    if self.grid[tuple(np.add(pos, BugWorld.MOVES[i]))]=='#':
                        c += 1
                if mygrid[pos] == '#' and c==1:
                    mygrid[pos] = '#'
                elif mygrid[pos] == '.' and (c==1 or c==2):
                    mygrid[pos] = '#'
                else:
                    mygrid[pos] = '.'
                    
        self.grid = mygrid.copy()
        
    
    def getBiodiversityRating(self):
        s = self.grid.shape
        mygrid = self.grid[1:s[0]-1, 1:s[1]-1]
        line = mygrid.flatten()
        r = 0
        for i in range(0, len(line)):
            if line[i]=='#':
                r+= 2**i
        return r
    

    def printMap(self):
        BugWorld.__printMap(self.grid)


#Part 1-----------------------------------------------------------------------

bs = set()
myworld = BugWorld("puzzle24.txt")

while(True):
    myworld.evolveOneStep()
    x = myworld.getBiodiversityRating()
    if x in bs:
        print("1----->", x)
        break
    bs.add(x)
    
    