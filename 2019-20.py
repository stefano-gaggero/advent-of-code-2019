# -*- coding: utf-8 -*-
"""
--- Day 20: Donut Maze ---

You notice a strange pattern on the surface of Pluto and land nearby to get a closer look. Upon closer inspection, you realize you've come across one of the famous space-warping mazes of the long-lost Pluto civilization!

Because there isn't much space on Pluto, the civilization that used to live here thrived by inventing a method for folding spacetime. Although the technology is no longer understood, mazes like this one provide a small glimpse into the daily life of an ancient Pluto citizen.

This maze is shaped like a donut. Portals along the inner and outer edge of the donut can instantly teleport you from one side to the other. For example:

         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       

This map of the maze shows solid walls (#) and open passages (.). Every maze on Pluto has a start (the open tile next to AA) and an end (the open tile next to ZZ). Mazes on Pluto also have portals; this maze has three pairs of portals: BC, DE, and FG. When on an open tile next to one of these labels, a single step can take you to the other tile with the same label. (You can only walk on . tiles; labels and empty space are not traversable.)

One path through the maze doesn't require any portals. Starting at AA, you could go down 1, right 8, down 12, left 4, and down 1 to reach ZZ, a total of 26 steps.

However, there is a shorter path: You could walk from AA to the inner BC portal (4 steps), warp to the outer BC portal (1 step), walk to the inner DE (6 steps), warp to the outer DE (1 step), walk to the outer FG (4 steps), warp to the inner FG (1 step), and finally walk to ZZ (6 steps). In total, this is only 23 steps.

Here is a larger example:

                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               

Here, AA has no direct path to ZZ, but it does connect to AS and CP. By passing through AS, QG, BU, and JO, you can reach ZZ in 58 steps.

In your maze, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ?

Your puzzle answer was 690.
"""

import numpy as np
import re

#Classe che rappresenta la mappa del labirinto
class MyMap:
    
    WALL = "#" 
    EMPTY = "."
    EXPLORED = "+"
    MOVES = [(0, 0), (-1, 0), (+1, 0), (0, -1), (0, +1)]
    

    @staticmethod
    def __printMap(m):
        s = ''
        for row in m:
            s = ''.join([c for c in row])
            print(s) 
    
    def __init__(self, fileName):
        
        self.portals = dict()
        self.portalsDir = dict()
        self.min = -1

        with open(fileName, "r") as f:
            self.rows = f.readlines()
            self.x = [ [str(c) for c in str(row) if c!='\n' ] for row in self.rows ]
            self.grid = np.array(self.x)
            
        self.columns = []
        cols = self.grid.transpose()  #Attenzione che il trasposto funziona solo per un 2D array e per essere tale le righe devono avere tutte la stessa lunghezza!
        for col in cols:
            self.columns.append(''.join(col))
            
        self.__findPortals()
        self.__createPortalsStruct()
        
        
    def __insertToPortals(self, key, val):
        if key not in self.portals:
            self.portals[key] = [val]
        else:
            self.portals[key].append(val)
    
    
    def __findPortals(self):
        rec = re.compile("(?:([A-Z]{2})\.{1})|(?:\.{1}([A-Z]{2}))")
        for i in range(0, len(self.rows)):
            matches = rec.finditer(self.rows[i])            
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (i,match.end(1)) )
                    
                if match.group(2) is not None:
                    self.__insertToPortals(match.group(2), (i, match.start(2)-1) )                    
                    
        for i in range(0, len(self.columns)):
            matches = rec.finditer(self.columns[i])            
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (match.end(1), i) )                    

                if match.group(2) is not None:
                    self.__insertToPortals(match.group(2), (match.start(2)-1, i) )
    
                
    def __createPortalsStruct(self):
        for key in self.portals:
            if key=="AA" or key=="ZZ":
                continue
            vals = self.portals[key]
            self.portalsDir[vals[0]] = vals[1]
            self.portalsDir[vals[1]] = vals[0]

    def explore(self):       
        k = 0
        startPos = self.portals["AA"][0]

        queue = [(startPos, 0)]
        while len(queue)>0:
            pos, k = queue.pop()        
            
            #Se la distanza già >= della siatnza minima registrata finora è inutile esplorare oltre
            if self.min!= -1 and k+1 >= self.min:  #Se la distanza già >= inutile esplorare oltre
                continue
                       
            for i in range(1, 5):
               newPos = tuple(np.add(pos, MyMap.MOVES[i]))
               x = self.grid[newPos]
                                   
               if newPos in self.portalsDir:
                   self.grid[newPos] = MyMap.EXPLORED
                   queue.insert(0, (self.portalsDir[newPos], k+2) )
                   
               elif newPos==self.portals["ZZ"][0]:
                   if self.min==-1 or k+1<self.min:
                       self.min = k+1                   
               
               elif x == MyMap.EMPTY:
                   queue.insert(0, (newPos, k+1) )
                   self.grid[newPos] = MyMap.EXPLORED
                   
        print("1---->" + str(self.min))  #690

        
    def printMap(self):
        MyMap.__printMap(self.grid)


#-----------------------------------------------------------------------------            
        
mymap = MyMap("puzzle20.txt")
mymap.explore()
#mymap.printMap()

