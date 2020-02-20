# -*- coding: utf-8 -*-
"""
--- Day 18: Many-Worlds Interpretation ---

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
        startPos = [(start[0][i], start[1][i]) for i in range(0,4)]
        for p in startPos:
            self.grid[p] = Node.EMPTY
        
        print("Start pos: " + str(startPos))
                   
        self.min = -1
        
        #Questa versione utilizza come chiave il set costituito dalle 4 chiavi simultanee dei 4 robot
        self.root = Node(self, startPos, 0, [64, 63, 62, 61], 0 )
        
        self.dct = dict()
        
        
    #Crea il grafico di tutti i percorsi possibili e contemporaneamente identifica quello con il percorso minore
    #Utilizza l'algoritmo BFS 
    def createGraph(self):
        fifo = [self.root]  #Si usa una coda FIFO per rendere più efficiente l'algoritmo di cache (in pratica prima si analizzano tutti i nodi allo stesso livello)
        k = 0
        
        while len(fifo)>0 and k<100000:
            k = k+1
            node = fifo.pop()
            
            #if k==2: print(str(k) + "--->" + str(node))
            
            if k%1000==0:
                print("--->" + str(k) + " " + str(len(fifo)) + " (" + str(len(node.keys)) + ")" )
                
            if not self.partialPathTestChkOnly(node): 
                continue
            
            debug = False
            #if k==2: debug = True
            node.explore(debug)
            #if k==2: print(str(k) + "------>" + str(node.children))            
            [fifo.insert(0, x) for x in node.children]
                    
        print("Done " + str(k))
        print("Residual: " + str(len(fifo)))
        
        
    #Questo metodo implementa una cache dei nodi visitati 
    #Un nodo visitato è identificato dalla chiave relativa al nodo e dalle chiavi raccolte nel percorso per raggiungere tale nodo
    #Per ogni entry è memorizzato il valore del percorso più breve per raggiungere tale nodo visitato
    #Restituisce True se il nodo passato come parametro ha un percorso minore
    #Questo metodo viene usato prima di inserire un nuovo nodo in modo da ridurre gli inserimenti
    def partialPathTest(self, node):
        key = frozenset(node.key)
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
#
#Nel caso di 4 robot, key e pos sono liste delle chiavi e delle posizioni dei 4 robot
#I nodi figli rappresentano tutte le possibili mosse dei 4 robot dalla posizione corrente        
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
              
    #Ogni nodo è identificato dalle 4 posizioni dei 4 robot, a loro volra identificate dalle chiavi in tale posizione
    #Nota che un nuovo nodo è creato solo quado uno dei robot aggiunge una chiave
    #index identifica quale robot ha cambiato la propria posizione
    def __init__(self, mymap, pos, d, key, index, parent = None):
        self.mymap = mymap
        self.grid = mymap.grid
        self.pos = pos
        self.d = d
        self.children = []
        self.key = key  #E' una lista delle 4 chiavi dei robot
        self.parent = parent        
                        
        if parent is not None: 
            self.keys = parent.keys.copy()
            self.moveList = parent.moveList.copy()
        else: 
            self.keys = set()
            self.moveList = []
            
        self.keys.add(key[index])
        self.moveList.append(str(index) + chr(key[index]) + "(" + str(self.d) + ")")
            
        self.toExplore = True  
        if len(self.keys) == mymap.keyNum + 1:  #Trovate tutte le chiavi in questo ramo
            self.toExplore = False              
            print("Found " + str(self.d) + ": " + str(self))
            if self.mymap.min==-1 or self.d<self.mymap.min:                
                self.mymap.min = self.d
                                                    
    def __str__(self):
        return str(self.moveList)
    
    def __repr__(self):
        return self.__str__()
        
    def doorKeysMatch(self, c):
        return (c+32) in self.keys

            
    def __explore(self, tmpGrid, keys, fifo, j, debug=False):       
        
        while len(fifo)>0:
            poss, k = fifo.pop()
                        
            #Se la distanza già >= della distanza minima registrata finora è inutile esplorare oltre
            if self.mymap.min!= -1 and k+1 > self.mymap.min:  #Se la distanza già >= inutile esplorare oltre
                continue
                        
            pos = poss[j]
                            
            for i in range(1, 5):

                                   
               newPos = tuple(np.add(pos, Node.MOVES[i]))
               
               
               x = tmpGrid[newPos]
               
               #if debug and j==0: print(str(i) + ": " + str(newPos))
               
               isKey = Node.__isKey(x)               
               if isKey: isNewKey = not x in self.keys
               else: isNewKey = False
               
               isDoor = Node.__isDoor(x)
               if isDoor: haveKey = self.doorKeysMatch(x)
               else: haveKey = False
               
               if x == Node.EMPTY or (isDoor and haveKey) or (isKey and not isNewKey):
                   newPoss = poss.copy()
                   newPoss[j] = newPos
                   
                   fifo.insert(0, (newPoss, k+1))
                   tmpGrid[newPos] = Node.EXPLORED
                   
               elif isNewKey:
                   ks = self.key.copy()
                   ks[j] = x
                   newPoss = poss.copy()
                   newPoss[j] = newPos
                   
                   node = Node(self.mymap, newPoss, k+1, ks, j, parent=self)
                   
                   if node.toExplore and self.mymap.partialPathTest(node):
                       self.children.append(node)    
                                                                    
    
    def explore(self, debug=False):
        if not self.toExplore:
            return
        
        #Se la distanza già >= della siatnza minima registrata finora è inutile esplorare oltre
        if self.mymap.min!= -1 and self.d > self.mymap.min:  
            return
        
        tmpGrid = self.grid.copy()
        for j in range(0,4):
            fifo = [(self.pos, self.d)]               
            self.__explore(tmpGrid, self.keys, fifo, j, debug)  
            
    
#------------------------------------------------------------------------------

m = MyMap("puzzle18b.txt")
#m = MyMap("test18b.txt") #72

print("key num: " + str(m.keyNum))
m.createGraph()
print("1----> "  + str(m.min))  #1828