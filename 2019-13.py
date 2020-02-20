# -*- coding: utf-8 -*-
import intcomputer as cmp
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

"""
--- Day 13: Care Package ---

As you ponder the solitude of space and the ever-increasing three-hour roundtrip for messages between you and Earth, you notice that the Space Mail Indicator Light is blinking. To help keep you sane, the Elves have sent you a care package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all the way on the other end of the ship. Surely, it won't be hard to build your own - the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your puzzle input). It has a primitive screen capable of drawing square tiles on a grid. The software draws tiles to the screen with output instructions: every three output instructions specify the x position (distance from the left), y position (distance from the top), and tile id. The tile id is interpreted as follows:

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?

--- Part Two ---

The game didn't run because you didn't put in any quarters. Unfortunately, you did not bring any quarters. Memory address 0 represents the number of quarters that have been inserted; set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right. The software reads the position of the joystick with input instructions:

    If the joystick is in the neutral position, provide 0.
    If the joystick is tilted to the left, provide -1.
    If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a single number that represents the player's current score. When three output instructions specify X=-1, Y=0, the third output instruction is not a tile; the value instead specifies the new score to show in the segment display. For example, a sequence of output values like -1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the last block is broken?

"""

class Cabinet:
    
    LEFT = -1
    RIGHT = +1
    NONE = 0
    
    def __init__(self, coin=-1):
        self.grid = np.zeros((26, 46))
        self.prog = cmp.loadFromFile("puzzle13.txt")
        self.score = 0
        self.ballPos = [-1, -1]
        self.prevBallPos = [-1, -1]
        self.paddlePos = [-1, -1]
        self.forecastBallsX = -1  #Posizione prevista palla sulla linea del pad
        if coin!=-1:
            self.prog.writeTo(0, coin)
            
            
    def __forecastBallsX(self):
        if self.prevBallPos[0]==-1: return -1
        stepY = self.ballPos[0] - self.prevBallPos[0]
        if stepY < 0: return -1  #Palla in allontanamento
        
        stepX = self.ballPos[1] - self.prevBallPos[1]  #Se >0, palla verso destra
        dy = self.paddlePos[0] - self.ballPos[0]  #Distanza verticale che manca dal paddle
        if dy<0: return -2  #Palla persa
        
        return int(self.ballPos[1] + stepX*dy)
        
    def run(self):
        self.prog.run()
        out = self.prog.getOutputs()
        res = np.reshape(out, (int(len(out)/3), 3))
        for x,y,i in res:
            if x==-1 and y==0:
                self.score = i
            else:
                self.grid[y, x] = i
                

        self.paddlePos = np.nonzero(self.grid==3)
        self.ballPos = np.nonzero(self.grid==4)
        self.forecastBallsX = self.__forecastBallsX()
        self.prevBallPos = list(self.ballPos).copy()

                
    def moveJoistick(self, val):
        self.prog.addInput(val)
        
            
    def moveJoistickToBall(self):
        if self.forecastBallsX<0: return         
        self.moveJoistick(-np.sign(self.paddlePos[1]-self.forecastBallsX))
        
    def endGame(self):
        return len(self.grid==2)==0
        
       

#Part 1----------------------------------------------------------------------
fig = plt.figure()


cab = Cabinet()
cab.run()
print(cab.prog.isEnded())
print(len(cab.grid[cab.grid==2]))  #324
plt.imshow(cab.grid)
plt.show()


#Part 2----------------------------------------------------------------------
camera = Camera(fig)            

cab = Cabinet(2)

k = 0
#Gioca finché non finisce il gioco
while not cab.prog.isEnded() and not cab.endGame() and k<10000:
    k = k + 1
    cab.run()    
    cab.moveJoistickToBall()
    if k<50:
        plt.imshow(cab.grid)
        camera.snap()        
    if k%1000==0:
        print("---> " + str(k) + " score---> " + str(cab.score))

animation = camera.animate()        
    
print(str(k) + " score---> " + str(cab.score))  #15957

#cab.saveAnimation('D:\\Lavoro\\Programmazione\\Python\\Adventofcode 2019\\day13animation.gif')
