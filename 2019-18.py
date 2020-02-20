# -*- coding: utf-8 -*-
"""
--- Day 18: Many-Worlds Interpretation ---

--- Part One ---


As you approach Neptune, a planetary security system detects you and activates a giant tractor beam on Triton! You have no choice but to land.

A scan of the local area reveals only one interesting feature: a massive underground vault. You generate a map of the tunnels (your puzzle input). The tunnels are too narrow to move diagonally.

Only one entrance (marked @) is present among the open passages (marked .) and stone walls (#), but you also detect an assortment of keys (shown as lowercase letters) and doors (shown as uppercase letters). Keys of a given letter open the door of the same letter: a opens A, b opens B, and so on. You aren't sure which key you need to disable the tractor beam, so you'll need to collect all of them.

For example, suppose you have the following map:

#########
#b.A.@.a#
#########

Starting from the entrance (@), you can only access a large door (A) and a key (a). Moving toward the door doesn't help you, but you can move 2 steps to collect the key, unlocking A in the process:

#########
#b.....@#
#########

Then, you can move 6 steps to collect the only other key, b:

#########
#@......#
#########

So, collecting every key took a total of 8 steps.

How many steps is the shortest path that collects all of the keys?

--- Part Two ---

You arrive at the vault only to discover that there is not one vault, but four - each with its own entrance.

On your map, find the area in the middle that looks like this:

...
.@.
...

Update your map to instead use the correct data:

@#@
###
@#@

This change will split your map into four separate sections, each with its own entrance:

#######       #######
#a.#Cd#       #a.#Cd#
##...##       ##@#@##
##.@.##  -->  #######
##...##       ##@#@##
#cB#Ab#       #cB#Ab#
#######       #######

Because some of the keys are for doors in other vaults, it would take much too long to collect all of the keys by yourself. Instead, you deploy four remote-controlled robots. Each starts at one of the entrances (@).

Your goal is still to collect all of the keys in the fewest steps, but now, each robot has its own position and can move independently. You can only remotely control a single robot at a time. Collecting a key instantly unlocks any corresponding doors, regardless of the vault in which the key or door is found.
"""

import numpy as np
import re
import sys

#Classe che rappresenta la mappa del labirinto
class MyMap:
    
    @staticmethod
    def printMap(m):
        s = ''
        for row in m:
            s = s + ''.join([c for c in row])
        print(s) 
        
    
    def __init__(self, fileName):

        self.keyNum = 0        
        rec = re.compile("[a-z]{1}")        
        with open(fileName, "r") as f:
            rows = f.readlines()
            for row in rows:
               self.keyNum = self.keyNum + len(rec.findall(row))
                
            self.grid = np.array([ [ord(c) for c in row ] for row in rows ])
            
        start = np.nonzero(self.grid==64)   #@                  
        startPos = (start[0][0], start[1][0])    
        
        print("Start pos: " + str(startPos))
        
        self.grid[startPos] = Node.EMPTY
        self.min = -1       
        
        self.root = Node(self, startPos, 0, 64)
        
        self.dct = dict()
        
        
    #Crea il grafico di tutti i percorsi possibili e contemporaneamente identifica quello con il percorso minore
    #Utilizza l'algoritmo BFS 
    def createGraph(self):
        fifo = [self.root]  #Si usa una coda FIFO per rendere più efficiente l'algoritmo di cache (in pratica prima si analizzano tutti i nodi allo stesso livello)
        k = 0
        
        while len(fifo)>0 and k<10000:
            k = k+1
            node = fifo.pop()
            
            if k%1000==0:
                print("--->" + str(k) + " " + str(len(fifo)) + " (" + str(len(node.keys)) + ")" )
                
            if not self.partialPathTestChkOnly(node): 
                continue
            
            node.explore()
            [fifo.insert(0, x) for x in node.children]
                    
        print("Done " + str(k))
        print("Residual: " + str(len(fifo)))
        
        
    #Questo metodo implementa una cache dei nodi visitati 
    #Un nodo visitato è identificato dalla chiave relativa al nodo e dalle chiavi raccolte nel percorso per raggiungere tale nodo
    #Per ogni entry è memorizzato il valore del percorso più breve per raggiungere tale nodo visitato
    #Restituisce True se il nodo passato come parametro ha un percorso minore
    #Questo metodo viene usato prima di inserire un nuovo nodo in modo da ridurre gli inserimenti
    def partialPathTest(self, node):
        key = node.key
        key2 = frozenset(node.keys)
        
        if key not in self.dct:
            #print("Create 1 " + str(key) + ", " + str(key2) + ": " + str(node.d))
            self.dct[key] = dict()
            self.dct[key][key2] = node.d
            return True
        
        dct2 = self.dct[key]
        
        if key2 not in dct2:
            #print("Create 2 " + str(key) + ", " + str(key2) + ": " + str(node.d))
            dct2[key2] = node.d
            return True
        
        val = dct2[key2]
        
        if val <= node.d:
            #print("Skip " + str(key) + ", " + str(key2) + ": " + str(node.d) + " (" + str(val) + ")")
            return False
        else:
            #print("Update " + str(key) + ", " + str(key2) + ": " + str(node.d))
            dct2[key2] = node.d
            return True
        
    #Testa solo in lettura la cache dei nodi visitati
    #Restituisce true se il percorso è minolre o UGUALE (se fosse solo minore non restituirebbe mai True)
    #Viene usato per testare il nodo appena prelevato dalla lista
    def partialPathTestChkOnly(self, node):        
        try:
            key = node.key
            key2 = frozenset(node.keys)
            val = self.dct[key][key2]
            return val>=node.d
        except:
            return True
    
            
    def print(self, clean=True):        
        MyMap.printMap(self.grid)
           

#Classe che rappresenta un nodo del grafo dei percorsi possibili
#Un nodo corrisponde un punto del labirinto in cui è presente una chiave
#Un nodo è caratterizzato anche dall'insieme delle chiavi raccolte durante il percorso e dunque dai nodi predecessori
#Tener traccia delle chiavi è indispensabile per determinare quali porte si possono aprire
#Inoltre, una volta raggiunto l'ultimo livello non è necessario riesplorare il grafo perchè il nodo contiene già la lunghezza del percorso
class Node:
        
    WALL = 35  # '#'
    EMPTY = 46 # '.'
    EXPLORED = 43 # '+'       
    MOVES = [(0, 0), (-1, 0), (+1, 0), (0, -1), (0, +1)]
        
    @staticmethod
    def __isKey(c):
        if c>=97 and c<=122: return True
        else: return False

    @staticmethod
    def __isDoor(c):
        if c>=65 and c<=90: return True
        else: return False
              
    
    def __init__(self, mymap, pos, d, key, parent = None):
        self.mymap = mymap
        self.grid = mymap.grid
        self.pos = pos
        self.d = d
        self.children = []
        self.key = key
        self.parent = parent        
                        
        if parent is not None: 
            self.keys = parent.keys.copy()            
        else: 
            self.keys = set()
            
        self.keys.add(key)
            
        self.toExplore = True  
        if len(self.keys) == mymap.keyNum+1:  #Trovate tutte le chiavi in questo ramo
            self.toExplore = False              
            if self.mymap.min==-1 or self.d<=self.mymap.min:
                print("Found " + str(self.d) + ": " + str(self))
                self.mymap.min = self.d
                                    
    def __str__(self):
        return str([chr(x) for x in self.keys])
    
    def __repr__(self):
        return self.__str__()
        
    def doorKeysMatch(self, c):
        return (c+32) in self.keys

            
    def __explore(self, tmpGrid, keys, fifo):       
        while len(fifo)>0:
            pos, k = fifo.pop()
            
            #Se la distanza già >= della siatnza minima registrata finora è inutile esplorare oltre
            if self.mymap.min!= -1 and k+1 >= self.mymap.min:  #Se la distanza già >= inutile esplorare oltre
                continue
                       
            for i in range(1, 5):
               newPos = tuple(np.add(pos, Node.MOVES[i]))
               x = tmpGrid[newPos]
               
               isKey = Node.__isKey(x)               
               if isKey: isNewKey = not x in self.keys
               else: isNewKey = False
               
               isDoor = Node.__isDoor(x)
               if isDoor: haveKey = self.doorKeysMatch(x)
               else: haveKey = False
               
               if x == Node.EMPTY or (isDoor and haveKey) or (isKey and not isNewKey):
                   fifo.insert(0, (newPos, k+1))
                   tmpGrid[newPos] = Node.EXPLORED
                   
               elif isNewKey:
                   node = Node(self.mymap, newPos, k+1, key=x, parent=self)
                   
                   if node.toExplore and self.mymap.partialPathTest(node):
                       self.children.append(node)
                   
    
    def explore(self):
        if not self.toExplore:
            return
        
        #Se la distanza già >= della siatnza minima registrata finora è inutile esplorare oltre
        if self.mymap.min!= -1 and self.d >= self.mymap.min:  
            return
        
        tmpGrid = self.grid.copy()
        fifo = [(self.pos, self.d)]               
        self.__explore(tmpGrid, self.keys, fifo)  
            
    
#------------------------------------------------------------------------------

m = MyMap("puzzle18.txt")
#m = MyMap("test18.txt")  #136

print("key num: " + str(m.keyNum))
m.createGraph()
print("1----> "  + str(m.min))  #4118