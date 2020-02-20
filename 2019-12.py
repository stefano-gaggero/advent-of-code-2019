# -*- coding: utf-8 -*-

import operator
import copy
from math import gcd

"""
--- Day 12: The N-Body Problem ---

Part 1:
The space near Jupiter is not a very safe place; you need to be careful of a big distracting red spot, extreme radiation, and a whole lot of moons swirling around. You decide to start by tracking the four largest moons: Io, Europa, Ganymede, and Callisto.

After a brief scan, you calculate the position of each moon (your puzzle input). You just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional velocity. The position of each moon is given in your scan; the x, y, and z velocity of each moon starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first update the velocity of every moon by applying gravity. Then, once all moons' velocities have been updated, update the position of every moon by applying velocity. Time progresses by one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z), the velocity of each moon changes by exactly +1 or -1 to pull the moons together. For example, if Ganymede has an x position of 3, and Callisto has a x position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5). However, if the positions on a given axis are the same, the velocity on that axis does not change for that pair of moons.

Once all gravity has been applied, apply velocity: simply add the velocity of each moon to its own position. For example, if Europa has a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3, then its new position would be x=-1, y=2, z=6. This process does not modify the velocity of any moon.

Then, it might help to calculate the total energy in the system. The total energy for a single moon is its potential energy multiplied by its kinetic energy. A moon's potential energy is the sum of the absolute values of its x, y, and z position coordinates. A moon's kinetic energy is the sum of the absolute values of its velocity coordinates.

What is the total energy in the system after simulating the moons given in your scan for 1000 steps?

--------------------------------------------------

Part 2:
    
Determine the number of steps that must occur before all of the moons' positions and velocities exactly match a previous point in time.    
   
Of course, the universe might last for a very long time before repeating. Here's a copy of the second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>

This set of initial positions takes 4686774924 steps before it repeats a previous state! Clearly, you might need to find a more efficient way to simulate the universe.
 
"""

class Moon:
    
    def __init__(self, pos):
        self.pos = pos
        self.vel = [0, 0, 0]
        self.pos0 = pos.copy()
        self.vel0 = [0, 0, 0]
        self.periods = [-1, -1, -1]
        
    def __eq__(self, other):
        return other.pos==self.pos and other.vel==self.vel

    def __str__(self):
        return "pos: " + str(self.pos) + " - vel: " + str(self.vel) + " (energy: " +str(self.getEnergy()) + ")"

    def __repr__(self):
        return "pos: " + str(self.pos) + " - vel: " + str(self.vel) + " (energy: " +str(self.getEnergy()) + ")"
        
    def getPosition(self):
        return self.pos.copy()
    
    def getVelocity(self):
        return self.vel.copy()    
    
    def updateVelocity(self, moons):
        for m in [m for m in moons if m!=self]:
            p0 = self.pos
            p1 = m.getPosition()
            for i in range(0, 3):
                if p0[i] > p1[i]: self.vel[i] = self.vel[i] - 1
                elif p0[i] < p1[i]: self.vel[i] = self.vel[i] + 1
        
    def applyVelocity(self):
        self.pos = list(map(operator.add, self.pos, self.vel))
        
    def getEnergy(self):
        return sum([abs(x) for x in self.pos]) * sum([abs(x) for x in self.vel])
        
    def isInInitialState(self, degreeOfFreedom):
        return self.pos[degreeOfFreedom]==self.pos0[degreeOfFreedom] and self.vel[degreeOfFreedom]==self.vel0[degreeOfFreedom]


def evolve(moons):
    for m in moons:
        m.updateVelocity(moons)
    for m in moons:
        m.applyVelocity()


#Per trovare il periodo di ripetizioni viene determinato il periodo di ogni grado di libertà e calcolato il mcm
#Questo riduce drasticamente le iterazioni necessarie
#Si basa sul fatto che i gradi di libertà sono indipendenti
def findPeriod(moons):
    periods = [-1, -1, -1]
    for i in range(0, 1000000):
        evolve(moons)
    
        for d in range(0,3):
            if  periods[d]==-1 and len([m for m in moons if not m.isInInitialState(d)])==0: #Tutte le lune sono nello stato iniziale
                periods[d] = i+1
                
        if len([p for p in periods if p!=-1])==3:
            break;
            
    print("Made " + str(i) + " iterations")
    
    lcm = periods[0]
    for p in periods:
        lcm = int(lcm*p/gcd(lcm, p))
        
    return lcm

       
#Test 1---------------------------------        
moons0 = []
moons0.append(Moon([-1, 0, 2]))
moons0.append(Moon([2, -10, -7]))
moons0.append(Moon([4, -8, 8]))
moons0.append(Moon([3, 5, -1]))

moons = copy.deepcopy(moons0)
for i in range(0, 10):
    """
    print("---> " + str(i))
    for m in moons:
        print(m)
    """    
    evolve(moons)       

totEnergy = sum([m.getEnergy() for m in moons])
print("Tot. final energy: " + str(totEnergy))  #179  

moons = copy.deepcopy(moons0)
p = findPeriod(moons)
            
print("Test 1: repeat after: " + str(p))  #2772


         
#Test 2---------------------------------        
moons = []
moons.append(Moon([-8, -10, 0]))
moons.append(Moon([5, 5, 10]))
moons.append(Moon([2, -7, 3]))
moons.append(Moon([9, -8, -3]))

p = findPeriod(moons)
            
print("Test 2: repeat after: " + str(p))  #4686774924
        
        
#Part 1---------------------------------        
moons0 = []
moons0.append(Moon([13, -13, -2]))
moons0.append(Moon([16, 2, -15]))
moons0.append(Moon([7, -18, -12]))
moons0.append(Moon([-3, -8, -8]))

moons = copy.deepcopy(moons0)
for i in range(0, 1000):
    evolve(moons)

totEnergy = sum([m.getEnergy() for m in moons])
print("Tot. final energy: " + str(totEnergy))   #12082  

#Part 2----------------------------------------------

moons = copy.deepcopy(moons0)
p = findPeriod(moons)
            
print("Repeat after: " + str(p))  #2772
