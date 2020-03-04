# -*- coding: utf-8 -*-
"""
--- Day 25: Cryostasis ---

As you approach Santa's ship, your sensors report two important details:

First, that you might be too late: the internal temperature is -40 degrees.

Second, that one faint life signature is somewhere on the ship.

The airlock door is locked with a code; your best option is to send in a small droid to investigate the situation. You attach your ship to Santa's, break a small hole in the hull, and let the droid run in before you seal it up again. Before your ship starts freezing, you detach your ship and set it to automatically stay within range of Santa's ship.

This droid can follow basic instructions and report on its surroundings; you can communicate with it through an Intcode program (your puzzle input) running on an ASCII-capable computer.

As the droid moves through its environment, it will describe what it encounters. When it says Command?, you can give it a single instruction terminated with a newline (ASCII code 10). Possible instructions are:

    Movement via north, south, east, or west.
    To take an item the droid sees in the environment, use the command take <name of item>. For example, if the droid reports seeing a red ball, you can pick it up with take red ball.
    To drop an item the droid is carrying, use the command drop <name of item>. For example, if the droid is carrying a green ball, you can drop it with drop green ball.
    To get a list of all of the items the droid is currently carrying, use the command inv (for "inventory").

Extra spaces or other characters aren't allowed - instructions must be provided precisely.

Santa's ship is a Reindeer-class starship; these ships use pressure-sensitive floors to determine the identity of droids and crew members. The standard configuration for these starships is for all droids to weigh exactly the same amount to make them easier to detect. If you need to get past such a sensor, you might be able to reach the correct weight by carrying items from the environment.

Look around the ship and see if you can find the password for the main airlock.

Your puzzle answer was 529920.

--- Part Two ---

As you move through the main airlock, the air inside the ship is already heating up to reasonable levels. Santa explains that he didn't notice you coming because he was just taking a quick nap. The ship wasn't frozen; he just had the thermostat set to "North Pole".

You make your way over to the navigation console. It beeps. "Status: Stranded. Please supply measurements from 49 stars to recalibrate."

"49 stars? But the Elves told me you needed fifty--"

Santa just smiles and nods his head toward the window. There, in the distance, you can see the center of the Solar System: the Sun!

"""

import intcomputer as cmp
import numpy as np

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


class Droid:
    
    UP = (-1, 0)
    DOWN = (+1, 0)
    LEFT = (0, -1)
    RIGHT = (0, +1)   
        
    def __init__(self):
        self.m = np.array([["." for x in range(0,13)] for y in range(0,13)])
        self.startPos = (6, 6)
        self.pos = self.startPos
        
        cmds = self.loadCmdHistory()               
        self.cpm = cmp.loadFromFile("puzzle25.txt")
        self.cpm.addInputs([ord(x) for x in cmds])
        self.cpm.run()

    def executeCommand(self, cmd, save=True, updateMap=True):
        cmd += chr(10)        
        if updateMap:
            self.updateMap(cmd)
        if save:         
            self.saveCmdHistory(cmd)
        self.cpm.addInputs([ord(x) for x in cmd])
        self.cpm.run()  
     
    def getOutput(self):
        return ''.join(map(str, [chr(x) for x in self.cpm.getOutputs(True)]))
        
    def printOutput(self):
        print(self.getOutput())


    def loadCmdHistory(self):
        f = open("cmdHistory.txt", "r")
        res = []
        for cmd in f.readlines():
            self.updateMap(cmd)
            res.extend(list(cmd))
        f.close()
        self.m[self.startPos] = "o"   
        return res        

    def saveCmdHistory(self, cmd):
        f = open("cmdHistory.txt", "a")
        f.write(cmd)
        f.close()  

    def updateMap(self, cmd):
        cmd = cmd.strip()
        if cmd=="north":
            self.m[self.pos] = "X"
            self.pos = tuple(np.add(self.pos,self.UP))
            self.m[self.pos] = "O"
            
        elif cmd=="south":
            self.m[self.pos] = "X"
            self.pos = tuple(np.add(self.pos,self.DOWN))
            self.m[self.pos] = "O"
            
        elif cmd=="east":
            self.m[self.pos] = "X"
            self.pos = tuple(np.add(self.pos,self.RIGHT))
            self.m[self.pos] = "O"
            
        elif cmd=="west":
            self.m[self.pos] = "X"
            self.pos = tuple(np.add(self.pos,self.LEFT))
            self.m[self.pos] = "O"
            
        self.m[self.startPos] = "o"   
        
        
    def tryObjs(self):
        objs = ["sand", "space heater", "loom", "wreath", "space law space brochure", "pointer", "planetoid", "festive hat"]
        
        #Prova un oggetto alla volta per eliminare subito quelli troppo pesanti
        objsCopy = objs.copy()
        for obj in objs:
            self.executeCommand("take " + obj, save=False, updateMap=False)
            self.executeCommand("north", save=False, updateMap=False)
            res = self.getOutput()
            if res.find("heavier")!=-1:
                print("try: ", obj, " lighter")
            elif res.find("lighter")!=-1:
                print("try: ", obj, " heavier")
                objsCopy.remove(obj)
            else:
                print("try: ", obj, " OK")
                break
            self.executeCommand("drop " + obj, save=False, updateMap=False)
            
        objs = objsCopy

        #Prova tutte le combinazioni degli oggetti rimanenti; la risposta è   529920      
        l = len(objs)
        jt = set()
        for i in range(0, l**l):
            selObjs = set(numberToBase(i, l))
            if frozenset(selObjs) in jt: 
                continue
            jt.add(frozenset(selObjs))
            for objIdx in selObjs:
                self.executeCommand("take " + objs[objIdx], save=False, updateMap=False)
            self.executeCommand("north", save=False, updateMap=False) 
               
            if res.find("heavier")!=-1:
                print("try: ", selObjs, " lighter")
            elif res.find("lighter")!=-1:
                print("try: ", selObjs, " heavier")
                objsCopy.remove(obj)
            else:
                print("try: ", selObjs, " OK")
                break
            
            for objIdx in selObjs:
                self.executeCommand("drop " + objs[objIdx], save=False, updateMap=False)
            
    def printMap(self):
        for row in self.m:
            print(''.join(map(str, row))) 
    

#-----------------------------------------------------------------------------
        
"""
La strategia è arrivare al punto chiave dove viene controllato il peso con tutti gli oggetti che è possibile raccogliere
Questo viene fatto a mano e il percoso viene salvato in cmdHistory per poterlo ripetere velocemente
A questo punto la funzione tryObjs() trova la combinazione corretta

Se si vuole ricominaciare daccapo occorre commentare tryObjs() e ripulire cmdHistory
"""
        
droid =  Droid()        
droid.tryObjs()

while True:
   
    droid.printOutput()    
    droid.printMap()
        
    cmd = input("---> ")
    
    if cmd=="bye":
        break
    else:
        droid.executeCommand(cmd)
        