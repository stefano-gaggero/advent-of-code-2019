# -*- coding: utf-8 -*-
"""
--- Day 17: Set and Forget ---

An early warning system detects an incoming solar flare and automatically activates the ship's electromagnetic shield. Unfortunately, this has cut off the Wi-Fi for many small robots that, unaware of the impending danger, are now trapped on exterior scaffolding on the unsafe side of the shield. To rescue them, you'll have to act quickly!

The only tools at your disposal are some wired cameras and a small vacuum robot currently asleep at its charging station. The video quality is poor, but the vacuum robot has a needlessly bright LED that makes it easy to spot no matter where it is.

An Intcode program, the Aft Scaffolding Control and Information Interface (ASCII, your puzzle input), provides access to the cameras and the vacuum robot. Currently, because the vacuum robot is asleep, you can only access the cameras.

Running the ASCII program on your Intcode computer will provide the current view of the scaffolds. This is output, purely coincidentally, as ASCII code: 35 means #, 46 means ., 10 starts a new line of output below the current one, and so on. (Within a line, characters are drawn left-to-right.)

In the camera output, # represents a scaffold and . represents open space. The vacuum robot is visible as ^, v, <, or > depending on whether it is facing up, down, left, or right respectively. When drawn like this, the vacuum robot is always on a scaffold; if the vacuum robot ever walks off of a scaffold and begins tumbling through space uncontrollably, it will instead be visible as X.

In general, the scaffold forms a path, but it sometimes loops back onto itself. For example, suppose you can see the following view from the cameras:

..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..

Here, the vacuum robot, ^ is facing up and sitting at one end of the scaffold near the bottom-right of the image. The scaffold continues up, loops across itself several times, and ends at the top-left of the image.

The first step is to calibrate the cameras by getting the alignment parameters of some well-defined points. Locate all scaffold intersections; for each, its alignment parameter is the distance between its left edge and the left edge of the view multiplied by the distance between its top edge and the top edge of the view. Here, the intersections from the above image are marked O:

..#..........
..#..........
##O####...###
#.#...#...#.#
##O###O###O##
..#...#...#..
..#####...^..

For these intersections:

    The top-left intersection is 2 units from the left of the image and 2 units from the top of the image, so its alignment parameter is 2 * 2 = 4.
    The bottom-left intersection is 2 units from the left and 4 units from the top, so its alignment parameter is 2 * 4 = 8.
    The bottom-middle intersection is 6 from the left and 4 from the top, so its alignment parameter is 24.
    The bottom-right intersection's alignment parameter is 40.

To calibrate the cameras, you need the sum of the alignment parameters. In the above example, this is 76.

Run your ASCII program. What is the sum of the alignment parameters for the scaffold intersections?

--- Part Two ---

Now for the tricky part: notifying all the other robots about the solar flare. The vacuum robot can do this automatically if it gets into range of a robot. However, you can't see the other robots on the camera, so you need to be thorough instead: you need to make the vacuum robot visit every part of the scaffold at least once.

The vacuum robot normally wanders randomly, but there isn't time for that today. Instead, you can override its movement logic with new rules.

Force the vacuum robot to wake up by changing the value in your ASCII program at address 0 from 1 to 2. When you do this, you will be automatically prompted for the new movement rules that the vacuum robot should use. The ASCII program will use input instructions to receive them, but they need to be provided as ASCII code; end each line of logic with a single newline, ASCII code 10.

First, you will be prompted for the main movement routine. The main routine may only call the movement functions: A, B, or C. Supply the movement functions to use as ASCII text, separating them with commas (,, ASCII code 44), and ending the list with a newline (ASCII code 10). For example, to call A twice, then alternate between B and C three times, provide the string A,A,B,C,B,C,B,C and then a newline.

Then, you will be prompted for each movement function. Movement functions may use L to turn left, R to turn right, or a number to move forward that many units. Movement functions may not call other movement functions. Again, separate the actions with commas and end the list with a newline. For example, to move forward 10 units, turn left, move forward 8 units, turn right, and finally move forward 6 units, provide the string 10,L,8,R,6 and then a newline.

Finally, you will be asked whether you want to see a continuous video feed; provide either y or n and a newline. Enabling the continuous video feed can help you see what's going on, but it also requires a significant amount of processing power, and may even cause your Intcode computer to overheat.

Due to the limited amount of memory in the vacuum robot, the ASCII definitions of the main routine and the movement functions may each contain at most 20 characters, not counting the newline.

For example, consider the following camera feed:

#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......

In order for the vacuum robot to visit every part of the scaffold at least once, one path it could take is:

R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2

Without the memory limit, you could just supply this whole string to function A and have the main routine call A once. However, you'll need to split it into smaller parts.

One approach is:

    Main routine: A,B,C,B,A,C
    (ASCII input: 65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10)
    Function A:   R,8,R,8
    (ASCII input: 82, 44, 56, 44, 82, 44, 56, 10)
    Function B:   R,4,R,4,R,8
    (ASCII input: 82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10)
    Function C:   L,6,L,2
    (ASCII input: 76, 44, 54, 44, 76, 44, 50, 10)

Visually, this would break the desired path into the following parts:

A,        B,            C,        B,            A,        C
R,8,R,8,  R,4,R,4,R,8,  L,6,L,2,  R,4,R,4,R,8,  R,8,R,8,  L,6,L,2

CCCCCCA...BBBBB
C.....A...B...B
C.....A...B...B
......A...B...B
......A...CCC.B
......A.....C.B
^AAAAAAAA...C.B
......A.A...C.B
......AAAAAA#AB
........A...C..
....BBBB#BBBB..
....B...A......
....B...A......
....B...A......
....BBBBA......

Of course, the scaffolding outside your ship is much more complex.

As the vacuum robot finds other robots and notifies them of the impending solar flare, it also can't help but leave them squeaky clean, collecting any space dust it finds. Once it finishes the programmed set of movements, assuming it hasn't drifted off into space, the cleaning robot will return to its docking station and report the amount of space dust it collected as a large, non-ASCII value in a single output instruction.

After visiting every part of the scaffold at least once, how much dust does the vacuum robot report it has collected?
"""

import intcomputer as cmp
import numpy as np
import matplotlib.pyplot as plt
import re

class Map:
    
    CF = 10 #A capo
    SC = 35 #Scaffold
    EM = 46 #Empty space
    FU = 94 #Face up
    SCV = 94  #Scaffold visited
    
    T = 0
    R = 1
    B = 2
    L = 3 
    
    DRS = [(-1,0),(0,1),(1,0),(0,-1)]
    
    def __init__(self):
        self.grid = None
        self.prog = cmp.loadFromFile("puzzle17.txt", [])
        self.startPos = (0,0)
        self.startDir = self.R
        
    def calc(self):
        self.prog.run()
        out = self.prog.getOutputs(True)
        cf = np.nonzero(np.array(out)==self.CF)  #Indici degli a capo

        x0 = 0
        k = 0
        row0 = []
        for x1 in cf[0]:
            if x1!=x0:
                row = out[x0:x1].copy()
                row.insert(0, self.EM)
                row.append(self.EM)
                if self.grid is None:
                    row0 = [self.EM for i in row]
                    self.grid = np.array(row0.copy())
                self.grid = np.vstack((self.grid, row))
            x0 = x1+1                  
        self.grid = np.vstack((self.grid, row0))
    
    #Già che scorre la griglia inizializza anche startPos
    def getSum(self):
        ss = 0
        for i in range(1, len(self.grid)-1):
            for j in range(1, len(self.grid[i])-1):
                x = self.grid[i][j]                
                n = self.grid[i-1][j]
                s = self.grid[i+1][j]
                e = self.grid[i][j+1]
                w = self.grid[i][j-1]                                
                if x==self.SC and n==self.SC and s==self.SC and e==self.SC and w==self.SC:
                    ss = ss + (i-1)*(j-1)
                    #self.grid[i][j] = 76
                if x!=self.SC and x != self.EM:
                    self.startPos = (i, j)
                    print(str(i) + ", " + str(j) + " - " + str(x) + " (" + chr(x) + ")")
        return ss
    
    def calcPath(self):
        #Dal momento che il puzzle è sempre uguale si da per assodato che startDir sia R 
        #e che la prima istruzione del percorso sia R         (dal momento che la direzione iniziale sarebbe T)
        pos = self.startPos
        dr = self.R
        path = ["R"]
        steps = 0
                
        while True:
            x = self.grid[tuple(np.add(pos, self.DRS[dr]))]
            if x==self.SC or x==self.SCV: 
                #Continua dritto
                #print("Continue to " + str(dr))
                pos = tuple(np.add(pos, self.DRS[dr]))
                self.grid[pos] = self.SCV
                steps = steps + 1
            else:
                #Gira a destra
                path.append(steps)
                path.append(",")
                steps = 0
                
                if   self.grid[ tuple(np.add(pos, self.DRS[(dr+1)%4])) ]==self.SC: #Prova a girare a destra
                    dr = (dr+1)%4
                    path.append("R")
                    #print("Turn R")
                elif self.grid[ tuple(np.add(pos, self.DRS[(dr-1)%4])) ]==self.SC: #Prova a girare a sinistra
                    dr = (dr-1)%4
                    path.append("L")
                    #print("Turn L")
                else:
                    print("Stop")
                    break  #Fine del percorso
        res = ''.join(map(str, path))
        self.path = res
            
    
    def draw(self):
        plt.imshow(self.grid)
        plt.show()
        
    def printOutput(self, clean=True):
        print(''.join(map(str, [chr(x) for x in self.prog.getOutputs(clean)])))
    
    #Trova tutte le possibili sottostringhe valide che iniziano con un comando (L o R) e finiscono con ,
    def findValidSubstrings(self, inStr):        
        if len(inStr.strip())==0: return []
        
        MAXL = 20
        l = len(inStr)
        d = set()
        for ls in range(MAXL+1, 6, -1): #ciclo su tutte le possibili dimensioni delle sottostringhe
            for i in range(0, l-ls+1):  #Cerca le sottostringhe nella stringa principale
                x = inStr[i:i+ls]
                
                if (x[0]!="R" and x[0]!="L") or x[ls-1]!="," or x.find(" ")!=-1: continue                    

                if x not in d: d.add(x)
                    
        return list(d)

        
    #Funzione ricorsiva per ordinare le sottostringhe nell'ordine in cui compaiono nella stringa principale
    #res alla fine contiene la lista degli indici allpinterno di substrs
    def orderSubstrings(self, inStr, substrs, res):
        if len(inStr)==0: return
        for i in range(0, len(substrs)):
            s = substrs[i]
            if inStr.find(s)==0:
                res.append(i)
                self.orderSubstrings(inStr[len(s):], substrs, res)
     
    def insertInputListToProd(self, lst):
        l = len(lst)  
        for i in range(0, l):
            val = lst[i]
            for c in val:
                self.prog.addInput(ord(c))
            if i<l-1:
                self.prog.addInput(ord(","))            
        self.prog.addInput(10)
        

    def insertInputStringToProg(self, val): 
        """
        #Non so perché non funziona!
        print("---->" + val)
        for c in val:
            self.prog.addInput(ord(c))
        self.prog.addInput(10)
        """
        rec = re.compile("([LR])([0-9]*)")
        lst = np.array(rec.findall(val)).flatten()
        self.insertInputListToProd(lst)
        
        
    def performStep2(self):
        #Stringa che corrisponde al percorso
        self.calcPath()
        m.draw()

        print("Stringa del percorso: " + self.path)
        
        #Trova i pattern ripetuti da assegnare alle movement functions e le ordina per lunghezza decrscente
        #Forza bruta, prova tutte le combinazioni
        inStr1 = self.path
        strs1 = self.findValidSubstrings(inStr1)
        found = False
                
        #Prova tutte le possibili combinazioni di 3 sottostringhe fino a trovare la prima giusta
        for str1 in strs1:
            inStr2 = inStr1.replace(str1, " ")
            strs2 = self.findValidSubstrings(inStr2)
            
            for str2 in strs2:
                inStr3 = inStr2.replace(str2, " ")            
                strs3 = self.findValidSubstrings(inStr3)
                for str3 in strs3:
                    inStr4 = inStr3.replace(str3, " ")
                    if len(inStr4.strip())==0: 
                        found = True
                    if found: break
                if found: break
            if found: break
    
        substrs = [str1, str2, str3]

        if not found: print("Errore!")           
        
        
        substrs = sorted(substrs, reverse=True, key=lambda item: len(item) )
        
        print("Movement functions: " + str(substrs))
        
        #Crea una lista con gli indici delle sottostringhe nell'ordine in cui compaiono nelle stringhe (sarà la main movement routine)
        substrsOrder = []
        self.orderSubstrings(self.path, substrs, substrsOrder)
        
        #Test della sottostringa:
        testList = [substrs[i] for i in substrsOrder]
        testStr = ''.join(map(str, testList))
        print("Test: " + str(testStr==self.path))
        
        programs=["A","B","C"]
        mainMovementRoutine = [programs[i] for i in substrsOrder]
        print("Main Movement Routine: " + str(mainMovementRoutine))
        
        #Esegue il programma
        self.prog = cmp.loadFromFile("puzzle17.txt", [])
        self.prog.program[0] = 2
        self.prog.run()
        self.printOutput()
        
        print("Add main movement routine: " + str(mainMovementRoutine))        
        self.insertInputListToProd(mainMovementRoutine)
        self.prog.run()
        
        
        for s in substrs:
            print("Add movement function: " + s) 
            self.insertInputStringToProg(s[:len(s)-1])
            self.prog.run()
            self.printOutput()
            
        print("Add n") 
        self.prog.addInput(ord("n"))
        self.prog.addInput(10)                     
        self.prog.run(False)
        
        #Questo visualizza l'eventuale errore        
        self.printOutput(False)
        
        return self.prog.getLastOutput()

    
#-----------------------------------------------------------------------------        
        
m = Map()
m.calc()

print("1---> " + str(m.getSum()))

out = m.performStep2()
print("2----> " + str(out))  #673996



