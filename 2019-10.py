"""
--- Day 10: Monitoring Station ---

Part 1:
    
You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.

The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).

The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).

Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.

For example, consider the following map:

.#..#
.....
#####
....#
...##

The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:

.7..7
.....
67775
....7
...87

Find the best location for a new monitoring station. How many other asteroids can be detected from that location?
"""

"""
Partendo da una griglia che ricopre il primo quadrante vengono calcolati tutti gli angoli dai punti della griglia all'origine
slots è un dictionary che contiene tutti gli angoli da 0 a 2\pi
In corrispondenza di ogni angolo c'è una lista dei punti della griglia attraversati dal semento con l'angolo dato
Vengono considerati solo i punti attraversati esattamente,  ma ogni angolo per costruzione contiene almeno un punto

------------------------------------------

Part 2:
    
Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the location and discover the worst: there are simply too many asteroids.

The only solution is complete vaporization by giant laser.

Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with a giant rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.

If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of them before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized, but if vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until the laser has returned to the same position by rotating a full 360 degrees.

The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate? (For example, 8,2 becomes 802.)
    
"""

import numpy as np
import math
import sys
  
def loadMap(fileName):
    f = open(fileName, "r")
    mymap = []
    for line in f:
        mymap.append(list(line.strip()))
    f.close()
    mymap = np.array(mymap)
    zs = np.zeros(mymap.shape)
    us = np.ones(mymap.shape)
    asteroids = np.transpose(np.nonzero(np.where(mymap=="#", us, zs)))
    print("Asteroids num: " + str(len(asteroids)))
    return [tuple(a) for a in asteroids], mymap
    
def insertToSlots(slots, a, pos):
    if a==2*np.pi: a = 0
    if a in slots:
        l = slots.get(a)
        if not pos in l: l.append(pos)
    else:
        slots[a] = [pos]        

#Crea un dictionary di tutti gli angoli possibili per un reticolo pari a 4 volte shape (ciascuno shape corrisponde a un quadrante)
#L'angolo ruota in senso orario, ed è pari a zero ad esempio per il punto (-1, 0)!
#l'angolo è la chiave, mentre l'oggetto è una lista di tuple contenenti le posizioni della grigia attraversate dal segmento con l'angolo dato
def initAngles(shape):
    slots = {}
    for y in range(0, shape[0]):
        for x in range(0, shape[1]):
            if x==0 and y==0: continue
            a = math.atan(x/y) if y!=0 else np.pi/2
            insertToSlots(slots, a, (-y, x) )  #Primo quadrante            
            if          a!= np.pi/2: insertToSlots(slots, np.pi - a  , [y, x] ) #Secondo quadrante
            if a!=0 and a!= np.pi/2: insertToSlots(slots, np.pi + a  , [y, -x] ) #Terzo quadrante            
            if a!=0                : insertToSlots(slots, 2*np.pi - a, [-y, -x] ) #Quarto quadrante
            
    
    #ordinamento di ciascuna lista in ordine di distanza DECRESCENTE (per far fuzionare il pop())
    for a in slots:
        slots[a] = sorted(slots[a], key=lambda pos : -pos[0]**2 - pos[1]**2)
        
    return slots


#Restituisce un dictionary di angoli e asterodi visti dal punto di vista di obj
def getRelativeSolots(obj, slots, asteroids):
    myslots = slots.copy()
    for a in myslots:
         myslots[a] = [(rel[0] + obj[0], rel[1] + obj[1]) for rel in myslots[a]]
         myslots[a] = [x for x in myslots[a] if x in asteroids] #Solo obj asterodi
    return myslots


#Restituisce il numero di asterodi visibili da obj
def getViews(obj, myslots):
    k = 0
    for a in myslots:
        if (len(myslots[a]))>0:
            k = k + 1        
    return k
  

def step1(asteroids, slots):            
    mx = 0
    mxp = None    
    for obj in asteroids:        
        myslots = getRelativeSolots(obj, slots, asteroids)
        k = getViews(obj, myslots)
        if k>mx:
            mx = k
            mxp = obj
            
    print(str(mxp) + ": " + str(mx))    
    return mxp


def step2(obj, asteroids, slots):
    myslots = getRelativeSolots(obj, slots, asteroids)
    
    k = 0
    mx = 200
    lastObj = None
    while k < mx:
        for a in sorted(list(myslots)):           
            if len(myslots[a]) > 0:                
                lastObj = myslots[a].pop()
                #print(str(k) + " : " + str(lastObj))
                k = k + 1
            if k==mx: break

    print("-->" + str(lastObj))
    print(lastObj[1]*100+lastObj[0])

        
asteroids, mymap = loadMap("puzzle10a.txt") 
slots = initAngles(mymap.shape)
baseObj = step1(asteroids, slots)  #274 (14, 19)
step2(baseObj, asteroids, slots) #305
