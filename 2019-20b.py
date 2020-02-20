# -*- coding: utf-8 -*-
"""
--- Part Two ---

Strangely, the exit isn't open when you reach it. Then, you remember: the ancient Plutonians were famous for building recursive spaces.

The marked connections in the maze aren't portals: they physically connect to a larger or smaller copy of the maze. Specifically, the labeled tiles around the inside edge actually connect to a smaller copy of the same maze, and the smaller copy's inner labeled tiles connect to yet a smaller copy, and so on.

When you enter the maze, you are at the outermost level; when at the outermost level, only the outer labels AA and ZZ function (as the start and end, respectively); all other outer labeled tiles are effectively walls. At any other level, AA and ZZ count as walls, but the other outer labeled tiles bring you one level outward.

Your goal is to find a path through the maze that brings you back to ZZ at the outermost level of the maze.

In the first example above, the shortest path is now the loop around the right side. If the starting level is 0, then taking the previously-shortest path would pass through BC (to level 1), DE (to level 2), and FG (back to level 1). Because this is not the outermost level, ZZ is a wall, and the only option is to go back around to BC, which would only send you even deeper into the recursive maze.

In the second example above, there is no path that brings you to ZZ at the outermost level.

Here is a more interesting example:

             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     


This path takes a total of 396 steps to move from AA at the outermost layer to ZZ at the outermost layer.

In your maze, when accounting for recursion, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ, both at the outermost layer?

Your puzzle answer was 7976.
"""

import numpy as np
import re

#Classe che rappresenta la mappa del labirinto
class MyMap:
    
    WALL = "#" 
    EMPTY = "."
    EXPLORED = "+"
    MOVES = [(0, 0), (-1, 0), (+1, 0), (0, -1), (0, +1)]
    OUTER = 0    
    INNER = 1

    @staticmethod
    def __printMap(m):
        s = ''
        for row in m:
            s = ''.join([c for c in row])
            print(s) 
    
    def __init__(self, fileName):       
        self.portalTypes = dict()
        self.portals = dict()
        self.portalsDir = dict()
        self.portalNames = dict()  #Solo per debug
        self.input = None
        self.output = None
        self.min = -1
        self.maxLevel = 0

        with open(fileName, "r") as f:
            self.rows = f.readlines()
            self.x = [ [str(c) for c in str(row) if c!='\n' ] for row in self.rows ]
            self.grid = np.array(self.x)
            
        #self.originalGrid = self.grid.copy()
        self.grid = np.repeat(self.grid[:, :, np.newaxis], 1000, axis=2)
            
        self.columns = []
        cols = self.grid[:,:,0].transpose()  #Attenzione che il trasposto funziona solo per un 2D array e per essere tale le righe devono avere tutte la stessa lunghezza!
        for col in cols:
            self.columns.append(''.join(col))
            
        self.__findPortals()
        self.__createPortalsStruct()
        
        
    def __insertToPortals(self, key, val, pType):
        if key=="AA":
            self.input = val
            return
        elif key=="ZZ":
            self.output = val
            return
        
        if key not in self.portals:
            self.portals[key] = [val]
        else:
            self.portals[key].append(val)
            
        self.portalTypes[val] = pType        
    
    
    def __findPortals(self):
        rec = re.compile("^([A-Z]{2})\.{1}")
        for i in range(0, len(self.rows)):
            matches = rec.finditer(self.rows[i])
            for match in matches:                
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (i,match.end(1)), MyMap.OUTER) #Esterni sinistri
        for i in range(0, len(self.columns)):   
            matches = rec.finditer(self.columns[i])
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (match.end(1), i), MyMap.OUTER) #Esterni superiori               

        rec = re.compile("\.{1}([A-Z]{2})\t?$")
        for i in range(0, len(self.rows)):
            matches = rec.finditer(self.rows[i])
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (i, match.start(1)-1), MyMap.OUTER) #Esterni destri            
        for i in range(0, len(self.columns)):            
            matches = rec.finditer(self.columns[i])            
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (match.start(1)-1, i), MyMap.OUTER) #Esterni inferiori

        rec = re.compile(" {1}([A-Z]{2})\.{1}")
        for i in range(0, len(self.rows)):
            matches = rec.finditer(self.rows[i])
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (i,match.end(1)), MyMap.INNER) #Interni destri            
        for i in range(0, len(self.columns)):            
            matches = rec.finditer(self.columns[i])            
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (match.end(1), i), MyMap.INNER) #Interni inferiori

        rec = re.compile("\.{1}([A-Z]{2}) {1}")
        for i in range(0, len(self.rows)):
            matches = rec.finditer(self.rows[i])
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (i, match.start(1)-1), MyMap.INNER) #Interni sinistri            
        for i in range(0, len(self.columns)):            
            matches = rec.finditer(self.columns[i])            
            for match in matches:
                if match.group(1) is not None:
                    self.__insertToPortals(match.group(1), (match.start(1)-1, i), MyMap.INNER) #Interni superiori
       
                
    def __createPortalsStruct(self):
        for key in self.portals:
            vals = self.portals[key]
            self.portalsDir[vals[0]] = vals[1]
            self.portalsDir[vals[1]] = vals[0]
            
            self.portalNames[vals[0]] = key  #Solo per debug
            self.portalNames[vals[1]] = key


    def explore(self):       
        k = 0
        queue = [(self.input, 0, 0)]       
            
        while len(queue)>0:
            
            #print("--------------->" + str(queue))
            
            pos, level, k = queue.pop()
            
            #Se la distanza già >= della siatnza minima registrata finora è inutile esplorare oltre
            if self.min!= -1 and k+1 >= self.min:  #Se la distanza già >= inutile esplorare oltre
                continue
                       
            for i in range(1, 5):
               newPos = tuple(np.add(pos, MyMap.MOVES[i]))
               x = self.grid[newPos][level]
                                   
               if newPos in self.portalsDir:
                   self.grid[newPos][level] = MyMap.EXPLORED
                   
                   if self.portalTypes[newPos] == MyMap.INNER:
                       newLevel = level + 1
                   else:
                       newLevel = level - 1                                          
                       
                   if newLevel > self.maxLevel: self.maxLevel = newLevel
                                              
                   if newLevel >= 0:                     
                       #print("Change from level "+ str(level) + " to level "+  str(newLevel) + " from portal " +  str(self.portalNames[newPos]) + "-->" + str(self.portalsDir[newPos]) + " (" + str(k) + ")" )
                       self.grid[self.portalsDir[newPos]][newLevel] = MyMap.EXPLORED
                       queue.insert(0, (self.portalsDir[newPos], newLevel, k+2) )                                          
                   
               elif newPos==self.output and level==0:
                   if self.min==-1 or k+1<self.min:
                       self.min = k+1                   
               
               elif x == MyMap.EMPTY:
                   queue.insert(0, (newPos, level, k+1) )
                   self.grid[newPos][level] = MyMap.EXPLORED
                           
        
    def printMap(self, idx=0):
        MyMap.__printMap(self.grid[:,:,idx])


#-----------------------------------------------------------------------------            
        
mymap = MyMap("puzzle20.txt")
mymap.explore()
mymap.printMap()
print("1---->" + str(mymap.min))  #7976
