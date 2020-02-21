# -*- coding: utf-8 -*-
"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /

In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L

Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I

In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.

Here, we can count the total number of orbits as follows:

    D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
    L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
    COM orbits nothing.

The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?

Your puzzle answer was 312697.
--- Part Two ---

Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN

Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)

Your puzzle answer was 466.
"""

"""
Ogni oggetto obj ha un puntatore all'oggetto intorno a cui orbita (tale relazione è univoca)

getNumDep(): restituisce il numero di oggetti totali intorno obj orbita direttamente e indirettamente
getDepsChain(): restituisce la lista sotto forma di codici stringa degli oggetti intorno obj orbita direttamente e indirettamente

objs è un dictionary con tutti gli oggetti nel puzzle

Per trovare il numero di passi tra un oggetto A e un oggetto B si percorre a ritroso la catena di A e di B fino a trovare un elemento comune
"""

class Obj:
    pointTo = None
    code = None
    
    def __init__(self, code):
        self.code = code
    
    def getNumDep(self):
        k = 0
        pt = self.pointTo
        while pt is not None:
            k = k + 1
            pt = pt.pointTo
        return k
    
    def getDepsChain(self):
        pt = self.pointTo
        ret = []
        while pt is not None:
            ret.append(pt.code)
            pt = pt.pointTo            
        return ret
    

objs = {}

f = open("puzzle06.txt", "r")    
for line in f:
    rel = line.split(")")
    code1 = rel[0]
    code2 = rel[1].strip()
    if code1 not in objs:
        objs[code1] = Obj(code1)        
    if code2 not in objs:
        objs[code2] = Obj(code2)        
        
    if objs[code2].pointTo is not None:
        print("Errore!")    
        break
    
    objs[code2].pointTo = objs[code1] 
f.close()  

k = 0
for code in objs:
    k = k + objs[code].getNumDep()

print("TOT count: " + str(k))

youDeps = objs["YOU"].getDepsChain()
sanDeps = objs["SAN"].getDepsChain()

ceNum = len(list(set(youDeps).intersection(sanDeps)))

stepsNum = len(youDeps) + len(sanDeps) - 2*ceNum

print("Steps to: " + str(stepsNum))
